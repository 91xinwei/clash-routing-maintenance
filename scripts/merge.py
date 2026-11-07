"""Merge maintained routing into an existing local config. Requires PyYAML."""
import pathlib,sys,yaml,os
src,out=map(pathlib.Path,sys.argv[1:]); d=yaml.safe_load(src.read_text())
assert src.resolve()!=out.resolve(), 'Use a separate output file'
root=pathlib.Path(__file__).resolve().parents[1]
template=yaml.safe_load((root/'config.example.yaml').read_text())
names=[g['name'] for g in d.get('proxy-groups',[])]
assert names, 'Input must contain existing proxy groups'
fallback=next((n for n in names if '手动' in n),names[0])
mapnames={}
for group in template['proxy-groups']:
 name=group['name']
 target=next((n for n in names if name.lower() in n.lower()),None)
 if not target:
  target='Routing '+name
  if target not in names:
   choices= [fallback] if name=='Proxy' else [mapnames.get(x,x) for x in group['proxies']]
   d['proxy-groups'].append({'name':target,'type':'select','proxies':choices}); names.append(target)
 mapnames[name]=target
providers=d.setdefault('rule-providers',{})
# Namespace providers so personal providers remain intact.
for name,value in template['rule-providers'].items(): providers['routing-'+name]=dict(value,path='./ruleset/routing-'+name+'.yaml')
new=[]
for rule in template['rules']:
 parts=rule.split(',')
 if parts[0]=='RULE-SET': parts[1]='routing-'+parts[1]
 pos=1 if parts[0]=='MATCH' else 2
 parts[pos]=mapnames.get(parts[pos],parts[pos]); new.append(','.join(parts))
# Preserve personal domain/process/port overrides before general managed rules.
old=[r for r in d.get('rules',[]) if not r.startswith('MATCH,') and r not in new and not r.startswith('RULE-SET,routing-')]
core=[r+','+mapnames['Claude'] for r in yaml.safe_load((root/'rules/claude.yaml').read_text())['payload']]
d['rules']=list(dict.fromkeys(core+old+new))
fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f: f.write(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
out.chmod(0o600)
print('Merged locally. Output contains private configuration; do not commit.')
