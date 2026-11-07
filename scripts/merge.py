"""Generate single-manual-group routing with local nodes. Requires PyYAML."""
import pathlib,sys,yaml,os
src,out=map(pathlib.Path,sys.argv[1:]); d=yaml.safe_load(src.read_text())
assert src.resolve()!=out.resolve(), 'Use a separate output file'
t=yaml.safe_load((pathlib.Path(__file__).resolve().parents[1]/'config.example.yaml').read_text())
# Keep node definitions and subscription providers, remove old policy chains.
blocked={'direct','reject','reject-drop','pass','compatible','dns'}
nodes=[p['name'] for p in d.get('proxies',[]) if p.get('type','').lower() not in blocked]
providers=list(d.get('proxy-providers',{}))
assert nodes or providers, 'No proxy nodes or subscription providers found'
g={'name':'手动选择','type':'select','proxies':nodes or ['REJECT']}
if providers: g['use']=providers
# DNS rules may reference removed groups; require an explicit update rather than silently retain them.
if d.get('sub-rules'): raise ValueError('Remove or migrate sub-rules before merging')
# Replace routing as a whole so old broad rules cannot bypass the new policy.
d['proxy-groups']=[g];d['rule-providers']=t['rule-providers'];d['rules']=t['rules'];d['mode']='rule'
fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f: f.write(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
out.chmod(0o600)
print('Generated single manual group. Private output: do not upload.')
