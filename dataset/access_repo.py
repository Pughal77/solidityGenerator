import requests
from datasets import Dataset, DatasetDict
import base64
import pandas as pd
from typing import Optional, Dict, List
import logging
from private_info import github_token

def fetch_readme_content(repo_id: str, repo_name: str, token: Optional[str] = None) -> Optional[str]:
    """
    Fetch README.md content from a GitHub repository.
    
    Args:
        repo_id (str): GitHub repository ID (username/organization)
        repo_name (str): Repository name
        token (str, optional): GitHub personal access token for authentication
    
    Returns:
        str: README content if found, None otherwise
    """
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Construct the API URL
    api_url = f"https://api.github.com/repos/{repo_id}/{repo_name}/contents/README.md"
    
    # Setup headers
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Decode the content
        content = response.json()
        if content.get("encoding") == "base64":
            readme_content = base64.b64decode(content["content"]).decode("utf-8")
            return readme_content
        else:
            logger.warning(f"Unexpected content encoding for {repo_id}/{repo_name}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching README for {repo_id}/{repo_name}: {str(e)}")
        return None

def create_readme_dataset(repo_data: List[Dict[str, str]], token: Optional[str] = None) -> DatasetDict:
    """
    Create a DatasetDict containing README contents from multiple repositories.
    
    Args:
        repo_data (List[Dict]): List of dictionaries containing repo_id and repo_name
        token (str, optional): GitHub personal access token
    
    Returns:
        DatasetDict: Dataset containing README contents
    """
    # Initialize lists to store data
    successful_repos = []
    readme_contents = []
    
    # Fetch README for each repository
    for repo in repo_data:
        content = fetch_readme_content(repo["repo_id"], repo["repo_name"], token)
        if content is not None:
            successful_repos.append(repo)
            readme_contents.append(content)
    
    # Create DataFrame
    df = pd.DataFrame(successful_repos)
    df["readme_content"] = readme_contents
    
    # Convert to Dataset and then to DatasetDict
    dataset = Dataset.from_pandas(df)
    dataset_dict = DatasetDict({
        "train": dataset  # You can split into train/test if needed
    })
    
    return dataset_dict

# Example usage
if __name__ == "__main__":
    # Example repository data
    repos = [
        {"repo_id": "huggingface", "repo_name": "transformers"},
        {"repo_id": "pytorch", "repo_name": "pytorch"}
    ]
    
    # Optional: Add your GitHub token here
    github_token =  github_token # "your_token_here"
    
    # Create dataset
    dataset_dict = create_readme_dataset(repos, github_token)
    
    # Print some information about the dataset
    print(f"Dataset size: {len(dataset_dict['train'])}")
    print("\nDataset features:", dataset_dict["train"].features)
    
    # Example: Print first README content
    if len(dataset_dict["train"]) > 0:
        print("\nFirst README preview:")
        print(dataset_dict["train"][0]["readme_content"][:200] + "...")