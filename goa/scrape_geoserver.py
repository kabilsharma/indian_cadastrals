import requests
import re
import json
import subprocess
import xmltodict
from bs4 import BeautifulSoup
from pathlib import Path
from pprint import pprint

epsg = "EPSG::32643"
MAX_RECORDS = 500
def run_external(cmd):
    print(f'running cmd - {cmd}')
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f'STDOUT: {res.stdout}')
        print(f'STDERR: {res.stderr}')
        raise Exception(f'command {cmd} failed with exit code: {res.returncode}')

data_dir = Path('data/')
data_dir.mkdir(exist_ok=True, parents=True)
base_url = "https://bhunakshawms.goa.gov.in/geoserver/dslr/ows"
params = { 
    "service": "WFS",
    "version": "1.0.0",
    "request": "GetFeature",
    "typeName": "dslr:khasramap",
    "maxFeatures": MAX_RECORDS,
    "outputFormat": "application/json"
}

def convert(feat):
    props = feat['properties']
    props['id'] = feat['id']
    props['geometry_name'] = feat['geometry_name']
    del feat['id']
    del feat['geometry_name']
    if 'attributes' not in props or props['attributes'] == '':
        return
    keep_attributes = False
    try:
        parsed = xmltodict.parse(props['attributes'])
    except:
        keep_attributes = True
        parsed = {}

    pairs =  parsed.get('attributes', {})\
                   .get('attribute', [])
    for pair in pairs:
        props[pair['@key']] = pair['@value']

    if not keep_attributes:
        del props['attributes']

batch_file = data_dir / 'batch.geojson'
batch_seq_file = data_dir / 'batch.geojsonl'

start_index = 0
total = 0
while True:
    params['startIndex'] = start_index
    resp = requests.get(base_url, params=params, verify=False)
    if not resp.ok:
        raise Exception(f'unable to get records for {start_index}')
    batch_file.unlink(missing_ok=True)
    batch_seq_file.unlink(missing_ok=True)

    data = json.loads(resp.text)
    feats = data['features']
    num = len(feats)
    total += num
    if num < MAX_RECORDS:
        break
    print(f'for {start_index} got {num} features, total={total}')
    
    batch_file.write_text(resp.text)
    run_external(f'ogr2ogr -f GeoJSONSeq {str(batch_seq_file)} {str(batch_file)}')
    with open('Goa_Cadastrals.geojsonl', 'a') as of:
        with open(batch_seq_file, 'r') as f:
            for line in f:
                feat = json.loads(line)
                convert(feat)
                of.write(json.dumps(feat))
                of.write('\n')


    start_index += MAX_RECORDS
