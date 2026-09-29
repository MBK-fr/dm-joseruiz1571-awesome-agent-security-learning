"""Shared catalog validation and URL normalization. Python standard library only."""
import hashlib
import ipaddress
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
TYPES = ['Research','Guides & standards','CTFs & labs','Courses','Certifications','Repositories & tools','Books','Blogs & newsletters','YouTube channels','Videos & webinars','Podcasts']
TOPICS = ['Security','Red teaming','Safety','Governance']
FAILURE_MODES = ['injection', 'goal-hijack', 'tool-exfil', 'identity', 'memory', 'traces/custody', 'scope/RoE', 'governance']
SCOPES = ['Agent-specific','Broader AI','Foundations']

def load(name):
    return json.loads((ROOT / 'data' / name).read_text())

def save(name, value):
    (ROOT / 'data' / name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

def canonical(url):
    p = urlsplit(url.strip())
    host = (p.hostname or '').lower()
    if p.scheme not in ('http','https') or not host or p.username or p.password:
        raise ValueError('Only public HTTP(S) URLs without credentials are allowed')
    if any(c in url for c in '\r\n\t<>"') or p.port not in (None,80,443):
        raise ValueError('Invalid URL characters or port')
    if host == 'localhost' or '.' not in host or host.endswith(('.local','.internal','.localhost')):
        raise ValueError('Local URLs are not allowed')
    try:
        if not ipaddress.ip_address(host).is_global:
            raise ValueError('Private addresses are not allowed')
    except ValueError as e:
        if str(e) == 'Private addresses are not allowed':
            raise
    path = p.path.rstrip('/')
    if host == 'github.com':
        path = path.lower().removesuffix('.git')
    query = urlencode(sorted((k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith('utm_') and k.lower() not in ('fbclid','gclid')))
    return urlunsplit(('https',host,path,query,''))

def resource_id(url):
    return hashlib.sha256(canonical(url).encode()).hexdigest()[:16]

def validate(resources):
    ids, urls = set(), set()
    for r in resources:
        for key in ['id','title','url','type','scope','cost','description','availability','evidence','verification']:
            if not isinstance(r.get(key),str) or not r[key].strip():
                raise ValueError(f'Missing or invalid {key}: {r.get("id")}')
        if r['id'] in ids or canonical(r['url']) in urls:
            raise ValueError(f'Duplicate resource: {r["id"]}')
        ids.add(r['id']); urls.add(canonical(r['url']))
        canonical(r['evidence'])
        if r['type'] not in TYPES or r['scope'] not in SCOPES:
            raise ValueError(f'Invalid classification: {r["id"]}')
        if not isinstance(r.get('topics'),list) or not r['topics'] or not set(r['topics']) <= set(TOPICS):
            raise ValueError('Invalid topics')
        modes = r.get('failure_modes', [])
        if not isinstance(modes, list) or any(not isinstance(m, str) or m not in FAILURE_MODES for m in modes) or len(modes) != len(set(modes)):
            raise ValueError('Invalid failure modes')
        if r.get('checked_on') is not None:
            date.fromisoformat(r['checked_on'])
        if r['verification'] not in ['Page inspected','Metadata only']:
            raise ValueError('Invalid verification')
    return resources

if __name__ == '__main__':
    print(f'Validated {len(validate(load("resources.json")))} resources')
