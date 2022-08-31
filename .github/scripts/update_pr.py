import requests
import sys
import os

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': "Bearer %s" % os.getenv('GITHUB_TOKEN')
}

data = {'title': sys.argv[1]}

repo_path = sys.argv[2]
pr_num = sys.argv[3]
url = "https://api.github.com/repos/%s/pulls/%s" % (repo_path, pr_num)

result = requests.patch(url, json=data, headers=headers)

if result.status_code > 299 or result.status_code < 200:
    print("\u001b[31mError %i: Failed to modify PR title: %s\u001b[0m" % (result.status_code, result.text))
    sys.exit(1)
