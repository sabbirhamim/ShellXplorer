import os
import readline
import rlcompleter

BUILTIN_WORDS = ["cd","pwd","ls","exit","jobs","kill","fg","help"]

def path_completions(text):
    # complete filesystem paths
    if not text:
        text = ""
    dirname = os.path.dirname(text) if os.path.dirname(text) else "."
    prefix = os.path.basename(text)
    try:
        entries = os.listdir(dirname)
    except Exception:
        return []
    suggestions = [os.path.join(dirname, e) + ("/" if os.path.isdir(os.path.join(dirname, e)) else "")
                   for e in entries if e.startswith(prefix)]
    return suggestions

def completer(text, state):
    # combine builtins and path completions
    options = [w for w in BUILTIN_WORDS if w.startswith(text)]
    options += path_completions(text)
    options = sorted(set(options))
    if state < len(options):
        return options[state]
    return None

def setup_readline():
    try:
        readline.set_completer(completer)
        readline.parse_and_bind('tab: complete')
    except Exception:
        pass
