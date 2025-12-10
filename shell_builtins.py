import os, shutil

# Full list of built‑in commands supported in ShellXplorer
BUILTINS = [
    "ls","cd","pwd","mkdir","rm","cp","cat",
    "history","!!","cpu","mem","ps","top","exit"
]

def run_builtin(tokens, history, monitor):
    cmd = tokens[0]

    # Change directory
    if cmd == "cd":
        try:
            os.chdir(tokens[1])
        except:
            print("Directory not found")

    # Print working directory
    elif cmd == "pwd":
        print(os.getcwd())

    # List current directory items
    elif cmd == "ls":
        print("\n".join(os.listdir()))

    # Create directory
    elif cmd == "mkdir":
        try:
            os.mkdir(tokens[1])
        except:
            print("Error: directory may already exist or invalid name")

    # Remove file
    elif cmd == "rm":
        try:
            os.remove(tokens[1])
        except:
            print("Error: file not found or permission denied")

    # Copy file
    elif cmd == "cp":
        try:
            shutil.copy(tokens[1], tokens[2])
        except:
            print("Copy failed — check file paths")

    # Display file contents
    elif cmd == "cat":
        try:
            print(open(tokens[1]).read())
        except:
            print("File not found or unreadable")

    # Display command history
    elif cmd == "history":
        history.show()

    # System monitor commands (CPU, RAM, process list, top)
    elif cmd in ["cpu", "mem", "ps", "top"]:
        monitor.run(cmd)

    # Exit shell
    elif cmd == "exit":
        print("Exiting ShellXplorer...")
        exit()
