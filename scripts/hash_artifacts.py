"""Refresh the manifest of maintained source, print artifacts and validation reports."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
files=[]
for folder in ['src','print','validation']:
 files += [p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json']
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(root/'validation/SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Hashed {len(manifest)} maintained files')
