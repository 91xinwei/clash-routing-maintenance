import concurrent.futures,pathlib,urllib.request,yaml
c=yaml.safe_load((pathlib.Path(__file__).resolve().parents[1]/'config.example.yaml').read_text())
assert c['proxy-groups']==[{'name':'手动选择','type':'select','proxies':['REJECT']}]
assert c['rules'][-1]=='MATCH,手动选择'
def check(item):
 name,p=item
 with urllib.request.urlopen(p['url'],timeout=45) as r: d=yaml.safe_load(r.read())
 assert isinstance(d.get('payload'),list) and d['payload'],name
 return name
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 print('Verified providers:',len(list(ex.map(check,c['rule-providers'].items()))))
for rule in c['rules']:
 p=rule.split(','); target=p[-2] if p[-1]=='no-resolve' else p[-1]
 assert target in ['DIRECT','REJECT','手动选择'],rule
print('Single manual group and rule targets OK')
