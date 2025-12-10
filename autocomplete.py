import os
import difflib

BUILTIN_COMMANDS = [
    "ls","cd","pwd","mkdir","rm","cp","cat",
    "history","!!","cpu","mem","ps","top","exit"
]

# Suggest commands starting with typed characters
def suggest_commands(text):
    return [cmd for cmd in BUILTIN_COMMANDS if cmd.startswith(text)]

# Suggest closest command if user mistypes
def fuzzy_suggest(text):
    return difflib.get_close_matches(text, BUILTIN_COMMANDS, cutoff=0.5)

# Suggest file or directory names (path auto complete)
def suggest_path(text):
    if "/" in text or "." in text:
        base = os.path.dirname(text) or "."
        prefix = os.path.basename(text)
    else:
        base = "."
        prefix = text

    try:
        return [f for f in os.listdir(base) if f.startswith(prefix)]
    except:
        return []
