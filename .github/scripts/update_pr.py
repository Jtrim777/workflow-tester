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

requests.patch(url, data=data, headers=headers)
