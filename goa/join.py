from pathlib import Path
import json

all_feats = []
for p in Path('.').glob('*.geojsonl'):
    lname = p.name.replace('.geojsonl', '')
    print(lname)
    with open(p, 'r') as f:
        for line in f:
            feat = json.loads(line)
            feat['properties']['lname'] = lname
            all_feats.append(feat)

print('writing out')
with open('all.geojsonl', 'w') as f:
    for feat in all_feats:
        f.write(json.dumps(feat))
        f.write('\n')
