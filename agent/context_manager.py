import os
import sys

CONTEXT_FILE = "/workspace/context.txt"
TOKEN_LIMIT = 1000000  # 1M tokens
BYTES_PER_TOKEN = 4
MAX_BYTES = TOKEN_LIMIT * BYTES_PER_TOKEN

def init():
    if not os.path.exists(CONTEXT_FILE):
        open(CONTEXT_FILE, 'w').close()

def append(text):
    with open(CONTEXT_FILE, 'a') as f:
        f.write(text + '\n')
    _prune()

def _prune():
    if os.path.getsize(CONTEXT_FILE) > MAX_BYTES:
        with open(CONTEXT_FILE, 'r') as f:
            lines = f.readlines()
        total_bytes = sum(len(line) for line in lines)
        index = 0
        while total_bytes > MAX_BYTES and index < len(lines):
            total_bytes -= len(lines[index])
            index += 1
        with open(CONTEXT_FILE, 'w') as f:
            f.writelines(lines[index:])

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "init":
        init()
    elif cmd == "append":
        append(sys.stdin.read())
