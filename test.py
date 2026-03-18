import subprocess
import os

cwd = r"c:\Users\Soumoditya Das\Downloads\GFG kolkata\frontend_extracted"
proc = subprocess.run(["npm.cmd", "run", "build"], cwd=cwd, capture_output=True, text=True)

with open(os.path.join(cwd, "build.log"), "w", encoding="utf-8") as f:
    f.write("===STDOUT===\n")
    f.write(proc.stdout)
    f.write("\n===STDERR===\n")
    f.write(proc.stderr)
