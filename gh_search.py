from github import Github
import os
from difflib import SequenceMatcher
import numpy as np
import tqdm
import argparse

# create a Github instance
g = Github(os.environ.get('GITHUB_TOKEN'))
MAX_COUNT = 300
MAX_LENGTH = 5000

# loop through every pull request in the repository
def pr_analysis(repo_name, file_name, desc_file_name, metadata_file_name=None):

    renamed_files_pr = []
    long_description_prs = []

    repo = g.get_repo(repo_name)
    prs = repo.get_pulls(state='all')
    total_prs = prs.totalCount

    count = 0
    for pr in tqdm.tqdm(prs, total=total_prs):
        # stop after MAX_COUNT pull requests
        count += 1
        if count >= MAX_COUNT:
            break

        # check the description of the PR, if it is longer than MAX_LENGTH, save it
        if pr.body is not None:
            if len(pr.body) > MAX_LENGTH:
                print(f'Found Long Description: {pr.title}')
                long_description_prs.append(pr.title)
                with open(desc_file_name, 'a+') as f:
                    f.write(f'{pr.title}\n')

        # check if the pull request deletes any files
        files_changed = pr.get_files()
        status_list = [file.status for file in files_changed]
        has_renamed = 'renamed' in status_list
        if has_renamed:
            # Add to renamed files list
            print(f'Found Renamed: {pr.title}')
            renamed_files_pr.append(pr.title)
            # Append to file, creating if it doesn't exist
            with open(file_name, 'a+') as f:
                f.write(f'{pr.title}\n')

    if metadata_file_name:
        # Print number of renamed file PRs and total PRs
        import json
        with open(metadata_file_name, 'a+') as f:
            json.dump({
                'repo_name': repo_name,
                'num_renamed_prs': len(renamed_files_pr),
                'num_prs': total_prs,
            }, f)

    return long_description_prs, renamed_files_pr


if __name__ == "__main__":
    list_of_top_oss_repos = [
        'tensorflow/tensorflow',
        'facebook/react'
        'angular/angular.js',
        'Microsoft/vscode',
        'twbs/bootstrap',
        'apple/swift',
        'apache/spark',
        'torvalds/linux',
        'nodejs/node',
        'ant-design/ant-design',
        'django/django',
        'laravel/laravel',
        'kubernetes/kubernetes',
        'microsoft/TypeScript',
    ]
    for repo in list_of_top_oss_repos:
        try:
            pr_analysis(repo, \
                        f'./data/{repo.replace("/", "_")}_renamed_prs.txt', \
                        f'./data/{repo.replace("/", "_")}_long_desc_prs.txt', \
                        f'./data/{repo.replace("/", "_")}_metadata.json')
        except Exception as e:
            print(f'Failed to get renamed PRs for {repo}')
            print(e)
            continue


