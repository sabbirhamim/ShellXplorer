import os
import shutil

def run_builtin(tokens, history, monitor):
    cmd = tokens[0]

    if cmd == "cd":
        try:
            os.chdir(tokens[1])
        except:
            print("Invalid directory")

    elif cmd == "pwd":
        print(os.getcwd())

    elif cmd == "ls":
        print("\n".join(os.listdir()))

    elif cmd == "mkdir":
        os.mkdir(tokens[1])

    elif cmd == "rm":
        os.remove(tokens[1])

    elif cmd == "cp":
        shutil.copy(tokens[1], tokens[2])

    elif cmd == "cat":
        with open(tokens[1]) as f:
            print(f.read())

    elif cmd == "history":
        history.show()

    elif cmd in ["cpu", "mem", "ps", "top"]:
        monitor.run(cmd)

    elif cmd == "exit":
        exit()

BUILTINS = ["cd","pwd","ls","mkdir","rm","cp","cat","history","cpu","mem","ps","top","exit"]
