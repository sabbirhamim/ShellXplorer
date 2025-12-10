#!/usr/bin/env python3
"""
ShellXplorer - main REPL
"""
import sys
import readline
from parser import parse_command
from executor import execute_parsed
from jobs import check_background_jobs, list_jobs, bring_job_foreground
from builtins import run_builtin, BUILTINS
from completer import setup_readline

PROMPT = "ShellXplorer> "

def main():
    print("🔥 ShellXplorer - Python educational shell")
    setup_readline()  # enable tab completion
    try:
        while True:
            check_background_jobs()
            try:
                line = input(PROMPT)
            except EOFError:
                print()  # newline on Ctrl-D
                break
            if not line.strip():
                continue

            parsed = parse_command(line)
            if parsed is None:
                continue

            # If single command and builtin, run builtin (supports jobs/fg/kill)
            if parsed["pipe_count"] == 0:
                cmd = parsed["commands"][0]
                if cmd and cmd[0] in BUILTINS:
                    try:
                        handled = run_builtin(cmd, parsed)
                        if handled is True:
                            continue
                    except SystemExit:
                        raise
                    except Exception as e:
                        print(f"❌ Builtin error: {e}")
                        continue

            # otherwise execute (could be external or pipeline)
            execute_parsed(parsed)

    except KeyboardInterrupt:
        print("\nType 'exit' to quit.")
    except SystemExit:
        pass
    finally:
        print("Goodbye.")

if __name__ == "__main__":
    main()
