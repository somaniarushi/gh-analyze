from github import Github
import os
from difflib import SequenceMatcher
import numpy as np
import tqdm
import argparse

# create a Github instance
g = Github(os.environ.get('GITHUB_TOKEN'))

# loop through every pull request in the repository
def pr_analysis(repo_name, file_name, desc_file_name, metadata_file_name, hyperparams):

    MAX_COUNT = hyperparams['count']
    MAX_LENGTH = hyperparams['length']

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
                'num_long_desc_prs': len(long_description_prs),
                'num_prs': total_prs,
            }, f)

    return long_description_prs, renamed_files_pr

def main():
    """
    Main function to run analysis
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description='Get repo name')
    # Required arguments
    parser.add_argument('repo', type=str, help='Name of repo to analyze')


    # Optional arguments
    parser.add_argument('--prs', type=int, default=True, help='Boolean to get PRs')
    parser.add_argument('--pr_count', type=int, default=100, help='Number of PRs to analyze')
    parser.add_argument('--pr_length', type=int, default=1000, help='Max length of PR description')

    parser.add_argument('--issues', type=int, default=True, help='Boolean to get issues')
    parser.add_argument('--issue_count', type=int, default=100, help='Number of issues to analyze')

    parser.add_argument('--commits', type=int, default=True, help='Boolean to get commits')
    parser.add_argument('--commit_count', type=int, default=100, help='Number of commits to analyze')

    parser.add_argument('--branches', type=int, default=True, help='Boolean to get comments')
    parser.add_argument('--branch_count', type=int, default=100, help='Number of branches to analyze')

    args = parser.parse_args()

    # Set variables
    repo_name = args.repo
    MAX_COUNT = args.count
    MAX_LENGTH = args.length

    if not repo_name:
        raise Exception('Repo name not provided')

    # Create file names
    file_name = f'./data/{repo_name.replace("/", "_")}_renamed_prs.txt'
    desc_file_name = f'./data/{repo_name.replace("/", "_")}_long_desc_prs.txt'
    metadata_file_name = f'./data/{repo_name.replace("/", "_")}_metadata.json'

    # Create hyperparams
    hyperparams = {
        'count': MAX_COUNT,
        'length': MAX_LENGTH,
    }

    # Run analysis
    pr_analysis(repo_name, file_name, desc_file_name, metadata_file_name, hyperparams)


if __name__ == "__main__":
    main()
