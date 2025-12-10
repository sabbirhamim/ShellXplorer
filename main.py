#!/usr/bin/env python3
import os
import shlex
import subprocess
import readline
from shell_builtins import BUILTINS, run_builtin
from history import History
from sysmonitor import SystemMonitor
from autocomplete import suggest_commands, suggest_path, fuzzy_suggest

history = History()
monitor = SystemMonitor()

# TAB Auto‑Completion
def complete(text, state):
    results = suggest_commands(text) + suggest_path(text)
    try:
        return results[state]
    except:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def execute_command(command):
    if command.strip():
        history.add(command)

    # history repeat
    if command == "!!":
        command = history.last()

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

    # Fuzzy suggestion if mistyped command
    if tokens[0] not in BUILTINS and "|" not in tokens:
        suggestion = fuzzy_suggest(tokens[0])
        if suggestion:
            print(f"Did you mean → {suggestion[0]} ?")

    # built‑ins
    if tokens[0] in BUILTINS:
        return run_builtin(tokens, history, monitor)

    # Redirection
    if ">" in tokens or "<" in tokens or ">>" in tokens:
        return executor_redirect(tokens)

    # Piping
    if "|" in tokens:
        return executor_pipe(tokens)

    # External commands
    try:
        subprocess.run(tokens)
    except FileNotFoundError:
        print("Command not found")

def executor_pipe(tokens):
    cmds, temp = [], []

    for t in tokens:
        if t == "|": cmds.append(temp); temp=[]
        else: temp.append(t)
    cmds.append(temp)

    prev=None
    for cmd in cmds:
        prev = subprocess.Popen(cmd, stdin=None if prev is None else prev.stdout, stdout=subprocess.PIPE)
    print(prev.communicate()[0].decode())

def executor_redirect(tokens):
    if ">" in tokens:
        index=tokens.index(">"); cmd=tokens[:index]; file=tokens[index+1]
        with open(file,"w") as f: subprocess.run(cmd,stdout=f)

    elif ">>" in tokens:
        index=tokens.index(">>"); cmd=tokens[:index]; file=tokens[index+1]
        with open(file,"a") as f: subprocess.run(cmd,stdout=f)

    elif "<" in tokens:
        index=tokens.index("<"); cmd=tokens[:index]; file=tokens[index+1]
        with open(file,"r") as f: subprocess.run(cmd,stdin=f)

def shell_loop():
    while True:
        try:
            cur=os.getcwd()
            prompt=f"\033[92mShellXplorer\033[0m:\033[94m{cur}\033[0m $ "
            command=input(prompt)
            execute_command(command)
        except (KeyboardInterrupt,EOFError):
            print("\nExiting ShellXplorer..")
            break

if __name__=="__main__":
    shell_loop()
