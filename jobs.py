import os
import time
from dataclasses import dataclass, field
from typing import List

@dataclass
class Job:
    id: int
    procs: List  # list of subprocess.Popen
    cmd: str
    started_at: float = field(default_factory=time.time)

_jobs = []
_next_id = 1

def add_background_job(procs, cmd):
    global _next_id
    job = Job(id=_next_id, procs=procs, cmd=cmd)
    _jobs.append(job)
    _next_id += 1

def check_background_jobs():
    # called periodically by main loop
    for job in _jobs[:]:
        all_done = True
        for p in job.procs:
            if p.poll() is None:
                all_done = False
                break
        if all_done:
            print(f"✔ Background job [{job.id}] finished: {job.cmd}")
            _jobs.remove(job)

def list_jobs():
    if not _jobs:
        print("No background jobs.")
        return
    for job in _jobs:
        statuses = []
        for p in job.procs:
            status = "running" if p.poll() is None else f"exit({p.returncode})"
            statuses.append(str(p.pid) + ":" + status)
        print(f"[{job.id}] {job.cmd} | " + ", ".join(statuses))

def find_job_by_id(jobid):
    for job in _jobs:
        if job.id == jobid:
            return job
    return None

def kill_job_by_pid(pid):
    try:
        os.kill(pid, 9)
        return True
    except Exception:
        return False

def bring_job_foreground(target):
    """
    target may be job id or pid (string)
    Wait on processes and remove job if present
    """
    # try job id first
    try:
        jid = int(target)
    except ValueError:
        jid = None

    if jid is not None:
        job = find_job_by_id(jid)
        if job:
            # wait for last process
            last = job.procs[-1]
            last.wait()
            print(f"Foreground: job [{job.id}] completed with code {last.returncode}")
            _jobs.remove(job)
            return

    # else try pid
    pid = None
    try:
        pid = int(target)
    except Exception:
        pass

    if pid:
        # wait for process with this pid if found
        for job in _jobs:
            for p in job.procs:
                if p.pid == pid:
                    p.wait()
                    print(f"Foreground: pid {pid} completed with code {p.returncode}")
                    # if all procs done, remove job
                    if all(pr.poll() is not None for pr in job.procs):
                        _jobs.remove(job)
                    return
    raise ValueError("No such job or pid")
