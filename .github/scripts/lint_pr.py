import re
import sys


def set_pr_title(new_name):
    """Exports the new PR title to GitHub Workflow's output detector"""
    print("::set-output name=new_title::"+new_name)


current_title = sys.argv[1]  # "${{ github.event.pull_request.title }}"
current_branch = sys.argv[2]  # "${{ github.head_ref }}"

ticket_branch_re = re.compile(r'^(\w\w-\d+)/.+')
fix_branch_re = re.compile(r'^fix/.+', flags=re.IGNORECASE)
chore_branch_re = re.compile(r'^chore/.+', flags=re.IGNORECASE)

fix_pr_re = re.compile(r'^HOTFIX \| .+')
chore_pr_re = re.compile(r'^Chore \| .+')

ticket_match = ticket_branch_re.match(current_branch)
if ticket_match:  # This is a ticket branch
    ticket = ticket_match.group(1).upper()

    if current_title.startswith(ticket + " | "):  # No changes necessary
        print("\u001b[32mPR Lint Successful\u001b[0m")
    else:  # Apply auto-fix to PR title
        title_text = re.sub(r'^%s[\s|/]*' % ticket, '', current_title, flags=re.IGNORECASE)
        print("\u001b[33mImproperly formatted PR title; Auto-applying fix\u001b[0m")
        set_pr_title("%s | %s" % (ticket, title_text))
elif fix_branch_re.match(current_branch):  # This is a hotfix branch
    if fix_pr_re.match(current_title):
        print("\u001b[33mPR Lint Successful, but use of un-ticketed PRs is not recommended\u001b[0m")
    else:
        title_text = re.sub(r'^(?:hot)?fix[\s|/]*', '', current_title, flags=re.IGNORECASE)
        print("\u001b[33mImproperly formatted PR title; Auto-applying fix\u001b[0m")
        set_pr_title("HOTFIX | %s" % title_text)
elif chore_branch_re.match(current_branch):  # This is a chore branch
    if chore_pr_re.match(current_title):
        print("\u001b[33mPR Lint Successful, but use of un-ticketed PRs is not recommended\u001b[0m")
    else:
        title_text = re.sub(r'^chore[\s|/]*', '', current_title, flags=re.IGNORECASE)
        print("\u001b[33mImproperly formatted PR title; Auto-applying fix\u001b[0m")
        set_pr_title("Chore | %s" % title_text)
else:  # This branch has a badly formed title
    print(("\u001b[31mError in PR Lint: \u001b[32m%s\u001b[31m is not a valid branch name. " % current_branch) +
          "Branches must start with a ticket ID, 'fix', or 'chore'\u001b[0m")
    sys.exit(1)
