import requests
def _submit_wrapper(urls, job_name, metric_name, metric_value, dimensions):
    dim = ''
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    for key, value in dimensions.items():
        dim += '/%s/%s' % (key, value)
    for url in urls:
        url__ = 'http://%s/metrics/job/%s%s' % (url, job_name, dim)
        print(url__)
        data = '%s %s\n' % (metric_name, metric_value)
        print(data)
        r = requests.post(url__,
                      data=data, headers=headers)
        print(r.text)

_submit_wrapper(["mschaffenroth.de:9091"], "weather", "temperature", "123", dimensions={})

