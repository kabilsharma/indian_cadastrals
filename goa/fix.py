import re
import json
import xmltodict
from pprint import pprint
from pathlib import Path

#attr_str = Path('temp.xml').read_text()
#pprint(attr_str)
#exit(0)

with open('Goa_Bhunaksha_Cadastrals.geojsonl.new', 'w') as of:
    with open('Goa_Bhunaksha_Cadastrals.geojsonl', 'r') as f:
        for line in f:
            feat = json.loads(line)
            props = feat['properties']
            if 'attributes' not in props or props['attributes'] is None or props['attributes'].strip() == '':
                of.write(json.dumps(feat))
                of.write('\n')
                continue
    
            attr_str = props['attributes']
            attr_str = attr_str.replace('\n', '')
            attr_str = attr_str.replace('<?xml version=1.0 encoding=UTF-8?>', '<?xml version="1.0" encoding="UTF-8"?>') 
            attr_str = attr_str.replace('value=/>', 'value= />')
            attr_str = re.sub(r'<attributekey=(.+?)value=(.+?)/>', '<attribute key="\\1" value="\\2"/>', attr_str)
            attr_str = re.sub(r'<attribute key=([^"]+?) value=([^"]+?)/>', '<attribute key="\\1" value="\\2"/>', attr_str)
            try:
                parsed = xmltodict.parse(attr_str)
            except:
                pprint(attr_str)
                Path('temp.xml').write_text(attr_str)
                raise
    
            pairs =  parsed.get('attributes', {})\
                           .get('attribute', [])
            for pair in pairs:
                props[pair['@key']] = pair['@value']
            del props['attributes']
            of.write(json.dumps(feat))
            of.write('\n')
