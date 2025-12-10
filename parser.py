import shlex

def parse_command(raw):
    """
    Returns dict:
      {
        "commands": [ [arg0, arg1, ...], ... ],  # one list per pipeline segment
        "background": bool,
        "pipe_count": int
      }
    """
    s = raw.strip()
    if not s:
        return None

    # background operator: last token '&' or trailing &
    background = False
    if s.endswith("&"):
        background = True
        s = s[:-1].rstrip()

    # naive syntax checks
    if s.startswith("|") or s.endswith("|"):
        print("❌ Syntax error: pipe at beginning or end")
        return None

    # split by pipe but allow quoted pipes via shlex: do manual split
    # simple approach: split on '|' and shlex.split each part
    parts = [p.strip() for p in s.split("|")]
    try:
        segments = [shlex.split(p) for p in parts if p != ""]
    except ValueError as e:
        print(f"❌ Parse error: {e}")
        return None

    return {
        "commands": segments,
        "background": background,
        "pipe_count": max(0, len(segments)-1)
    }
