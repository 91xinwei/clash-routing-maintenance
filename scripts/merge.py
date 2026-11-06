"""Usage: python scripts/merge.py INPUT.yaml OUTPUT.yaml; requires PyYAML."""
import pathlib,sys,yaml
src,out=map(pathlib.Path,sys.argv[1:]); d=yaml.safe_load(src.read_text())
assert src.resolve()!=out.resolve(), 'Use a separate output file'
names=[g['name'] for g in d.get('proxy-groups',[])]
assert names, 'Input must contain existing proxy groups'
target=next((n for n in names if 'claude' in n.lower()),None)
if not target:
 target='Claude'; d['proxy-groups'].append({'name':target,'type':'select','proxies':[names[0]]})
r=yaml.safe_load((pathlib.Path(__file__).resolve().parents[1]/'rules/claude.yaml').read_text())['payload']
prefix=[x+','+target for x in r]
d['rules']=prefix+[x for x in d.get('rules',[]) if x not in prefix]
out.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False)); out.chmod(0o600)
print('Merged locally; output contains private configuration. Do not commit it.')
