import json
import os

from github import Github
import requests


def read_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def get_actions_input(input_name):
    return os.getenv('INPUT_{}'.format(input_name).upper())


def main():
    gh = Github(os.getenv('GITHUB_TOKEN'))
    event = read_json(os.getenv('GITHUB_EVENT_PATH'))
    branch_label = event['pull_request']['head']['label']  # author:branch
    repo = gh.get_repo(event['repository']['full_name'])
    prs = repo.get_pulls(state='open', sort='created', head=branch_label)
    pr = prs[0]

    response = requests.get(
        "https://api.hypervector.io/v1/assertions/last",
        headers={"x-api-key": get_actions_input("HYPERVECTOR_API_KEY")}
    )

    assertion = response.json()
    bencmark_uuid = assertion['benchmark_uuid']
    hypervector_link = f"https://dashboard.hypervector.io/benchmark/{bencmark_uuid}"

    if assertion['asserted'] is True:
        result_icon = '✅ PASSED'
    else:
        result_icon = '❌ FAILED'

    comment = f"{result_icon}\n" \
              f"```json\n" \
              f"{json.dumps(assertion, indent=2)}\n" \
              f"```\n\n" \
              f"View assertion history on Hypervector: {hypervector_link}"

    pr.create_issue_comment(comment)


if __name__ == '__main__':
    main()
