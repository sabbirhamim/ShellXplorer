import subprocess
import os
from jobs import add_background_job

def execute_parsed(parsed):
    """
    Execute single command or pipeline.
    If background flag is set, do not wait and record job.
    """
    commands = parsed["commands"]
    background = parsed["background"]

    procs = []
    prev_stdout = None

    for i, cmd in enumerate(commands):
        # if empty cmd (shouldn't happen) skip
        if not cmd:
            continue

        # if last command capture output to print; else pipe to next
        is_last = (i == len(commands) - 1)
        stdout = subprocess.PIPE if not is_last else subprocess.PIPE

        try:
            p = subprocess.Popen(
                cmd,
                stdin=prev_stdout,
                stdout=stdout,
                stderr=subprocess.PIPE,
                text=True
            )
        except FileNotFoundError:
            print(f"❌ Command not found: {cmd[0]}")
            # cleanup previous processes
            for proc in procs:
                try:
                    proc.kill()
                except Exception:
                    pass
            return
        except Exception as e:
            print(f"❌ Failed to start {cmd[0]}: {e}")
            for proc in procs:
                try:
                    proc.kill()
                except Exception:
                    pass
            return

        procs.append(p)
        # close previous stdout in parent, pass as stdin to next
        if prev_stdout is not None and prev_stdout != subprocess.PIPE:
            try:
                prev_stdout.close()
            except Exception:
                pass
        prev_stdout = p.stdout

    # If background: register job and return immediately
    if background:
        add_background_job(procs, " | ".join([" ".join(c) for c in commands]))
        print(f"🟢 Background job started: PID {procs[-1].pid}")
        return

    # Foreground: wait for pipeline to complete, then print last output
    last = procs[-1]
    stdout, stderr = last.communicate()
    # Wait for others to finish
    for p in procs[:-1]:
        p.wait()

    if stdout:
        print(stdout, end="")
    if stderr:
        # decode and print last process stderr
        print(stderr, end="")
