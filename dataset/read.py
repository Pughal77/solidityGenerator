import pyarrow.parquet as pq

# python file to read parquet file downloaded from 
# @misc {seyyed_ali_ayati_2023,
# 	author       = { {Seyyed Ali Ayati} },
# 	title        = { solidity-dataset (Revision 77e80ad) },
# 	year         = 2023,
# 	url          = { https://huggingface.co/datasets/seyyedaliayati/solidity-dataset },
# 	doi          = { 10.57967/hf/0808 },
# 	publisher    = { Hugging Face }
# }
parquet_file = pq.ParquetFile('./dataset/set1.parquet')
df = parquet_file.read().to_pandas()

df.to_csv('set1.csv', index=False)

print(df.head())

# to read through list of repos for their respective readmes
import requests
import base64

# GitHub API endpoint
api_url = "https://api.github.com"

# Your GitHub personal access token
token = "YOUR_PERSONAL_ACCESS_TOKEN"

# Headers for authentication
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

def get_readme_content(owner, repo):
    readme_url = f"{api_url}/repos/{owner}/{repo}/readme"
    response = requests.get(readme_url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()["content"]
        decoded_content = base64.b64decode(content).decode("utf-8")
        return decoded_content
    else:
        return None

# List of repositories to search
repos = [
    {"owner": "owner1", "repo": "repo1"},
    {"owner": "owner2", "repo": "repo2"},
    # Add more repositories as needed
]

# Iterate through the repositories and fetch README contents
for repo in repos:
    readme_content = get_readme_content(repo["owner"], repo["repo"])
    if readme_content:
        print(f"README for {repo['owner']}/{repo['repo']}:")
        print(readme_content)
        print("-" * 50)
    else:
        print(f"README not found for {repo['owner']}/{repo['repo']}")
        print("-" * 50)
