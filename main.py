#!/usr/bin/env python3
import os
import shlex
import subprocess
from shell_builtins import BUILTINS, run_builtin
from history import History
from sysmonitor import SystemMonitor

history = History()
monitor = SystemMonitor()

def execute_command(command):
    # History support
    if command.strip():
        history.add(command)

    # !! repeat last command
    if command == "!!":
        command = history.last()
        print(f"Re-running: {command}")

    # !n run specific history command
    if command.startswith("!"):
        try:
            index = int(command[1:])
            command = history.get(index)
        except:
            print("Invalid history reference")
            return

    tokens = shlex.split(command)
    if not tokens:
        return

    # Built-in command
    if tokens[0] in BUILTINS:
        return run_builtin(tokens, history, monitor)

    # I/O Redirection
    if ">" in tokens or "<" in tokens or ">>" in tokens:
        return executor_redirect(tokens)

    # Pipeline Support |
    if "|" in tokens:
        return executor_pipe(tokens)

    try:
        subprocess.run(tokens)
    except FileNotFoundError:
        print("Command not found")

def executor_pipe(tokens):
    cmds = []
    temp = []

    for token in tokens:
        if token == "|":
            cmds.append(temp)
            temp = []
        else:
            temp.append(token)
    cmds.append(temp)

    prev = None
    for cmd in cmds:
        if prev is None:
            prev = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        else:
            prev = subprocess.Popen(cmd, stdin=prev.stdout, stdout=subprocess.PIPE)
    output = prev.communicate()[0]
    print(output.decode())

def executor_redirect(tokens):
    if ">" in tokens:
        index = tokens.index(">")
        outfile = tokens[index + 1]
        cmd = tokens[:index]
        with open(outfile, "w") as f:
            subprocess.run(cmd, stdout=f)
    elif ">>" in tokens:
        index = tokens.index(">>")
        outfile = tokens[index + 1]
        cmd = tokens[:index]
        with open(outfile, "a") as f:
            subprocess.run(cmd, stdout=f)
    elif "<" in tokens:
        index = tokens.index("<")
        infile = tokens[index + 1]
        cmd = tokens[:index]
        with open(infile, "r") as f:
            subprocess.run(cmd, stdin=f)

def shell_loop():
    while True:
        try:
            current = os.getcwd()
            prompt = f"\033[92mShellXplorer\033[0m:\033[94m{current}\033[0m $ "
            command = input(prompt)
            execute_command(command)
        except (KeyboardInterrupt, EOFError):
            print("\nExit Shell")
            break

if __name__ == "__main__":
    shell_loop()
