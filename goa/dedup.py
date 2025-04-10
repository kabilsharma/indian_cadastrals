from pathlib import Path
import json
import os
import sys

def dedup(inp_file):
    deduped_file = Path(str(inp_file) + '.deduped')
    lines = {}
    with open(deduped_file, 'w') as of:
        with open(inp_file, 'r') as f:
            count = 0
            for line in f:
                try:
                    feat = json.loads(line)
                except Exception:
                    print(count)
                    print(line)
                    raise
                count += 1
                props = feat['properties']
                geom = feat['geometry']
                gtype = geom['type']
                if gtype not in ['MultiPolygon', 'Polygon']:
                    continue
                s = json.dumps(feat)
                if s in lines:
                    print(f'current: {props} prev: {lines[s]}')
                    continue

                lines[s] = props
                of.write(line)
    inp_file.unlink()
    os.rename(str(deduped_file), str(inp_file))


fname = sys.argv[1]
print(f'deduping {fname}')
dedup(Path(fname))
