import os
import signal
import sys
from jobs import list_jobs, kill_job_by_pid, bring_job_foreground

BUILTINS = {"cd", "pwd", "ls", "exit", "jobs", "kill", "fg", "help"}

def run_builtin(cmd_args, parsed=None):
    """
    Execute a builtin command.
    Return True if handled. For exit, raise SystemExit.
    """
    if not cmd_args:
        return True

    cmd = cmd_args[0]
    if cmd == "cd":
        path = cmd_args[1] if len(cmd_args) > 1 else os.path.expanduser("~")
        try:
            os.chdir(path)
        except FileNotFoundError:
            print("❌ cd: directory not found")
        except NotADirectoryError:
            print("❌ cd: not a directory")
        return True

    if cmd == "pwd":
        print(os.getcwd())
        return True

    if cmd == "ls":
        # simple ls: no flags parsing
        target = cmd_args[1] if len(cmd_args) > 1 else "."
        try:
            for name in sorted(os.listdir(target)):
                print(name)
        except Exception as e:
            print(f"❌ ls: {e}")
        return True

    if cmd == "exit":
        raise SystemExit(0)

    if cmd == "help":
        print("Builtins:", ", ".join(sorted(BUILTINS)))
        print("Supports pipes and background (&). Use 'jobs', 'fg <jobid|pid>', 'kill <pid|signal>'.")
        return True

    if cmd == "jobs":
        list_jobs()
        return True

    if cmd == "kill":
        if len(cmd_args) < 2:
            print("❌ kill: usage: kill <pid> or kill -SIG pid")
            return True
        # support "kill PID" or "kill -9 PID"
        args = cmd_args[1:]
        try:
            if args[0].startswith("-") and len(args) >= 2:
                sig = int(args[0][1:])
                pid = int(args[1])
                os.kill(pid, sig)
            else:
                pid = int(args[0])
                os.kill(pid, signal.SIGTERM)
        except Exception as e:
            print(f"❌ kill: {e}")
        return True

    if cmd == "fg":
        # bring job/pid to foreground
        if len(cmd_args) < 2:
            print("❌ fg: usage: fg <jobid|pid>")
            return True
        target = cmd_args[1]
        try:
            bring_job_foreground(target)
        except Exception as e:
            print(f"❌ fg: {e}")
        return True

    return False
