from pathlib import Path

for f in Path('uploads').glob('*'):
    if f.is_file():
        f.unlink()

for f in Path('temp').glob('*'):
    if f.is_file():
        f.unlink()
