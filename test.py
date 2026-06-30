from pathlib import Path

path = Path.cwd() / "temp/pgg"

suppurted_files = [".docx", "doc"]

for file in path.rglob("*"):
    if file.suffix in suppurted_files:
        print(file)