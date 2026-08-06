import time, json, urllib.request

def get(url):
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.github+json')
    return urllib.request.urlopen(req, timeout=15).read().decode()

deadline = time.time() + 1500
verdict = None
while time.time() < deadline:
    try:
        runs = json.loads(get('https://api.github.com/repos/jialeCharloote/ai-daily-page/actions/runs?per_page=1'))
        r = runs['workflow_runs'][0]
        if r['status'] == 'completed':
            verdict = (r['head_sha'][:7], r['conclusion'])
            break
    except Exception as e:
        print('api:', e, flush=True)
    time.sleep(30)

print('FINAL DEPLOY:', verdict, flush=True)

if verdict and verdict[1] == 'success':
    for i in range(10):
        url = 'https://jialecharloote.github.io/ai-daily-page/?cb=%d' % int(time.time())
        req = urllib.request.Request(url)
        req.add_header('Cache-Control', 'no-cache')
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'replace')
        if 'Millennium' in html:
            print('SITE LIVE with evening version', flush=True)
            break
        time.sleep(15)
    else:
        print('deploy success but site still serving old version', flush=True)
