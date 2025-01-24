import requests
from datasets import DatasetDict
import base64
from typing import Optional
import logging



class TransformedDataset:
    def __init__(self, gh_token, dataset: DatasetDict, num_train_examples: int = 300):
        self.gh_token = gh_token
        assert(num_train_examples >= 10)
        self.train_set = dataset['train'].select(range(num_train_examples))
        self.test_set = dataset['test'].select(range(int(num_train_examples * 0.1)))
        self.eval_set = dataset['eval'].select(range(int(num_train_examples * 0.1)))
        self.create_readme_dataset(self.gh_token)


    def fetch_readme_content(self, repo_name: str) -> Optional[str]:
        """
        Fetch README.md content from a GitHub repository.
        
        Args:
            repo_name (str): Repository name
            token (str, optional): GitHub personal access token for authentication
        
        Returns:
            str: README content if found, None otherwise
        """
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Construct the API URL
        api_url = f"https://api.github.com/repos/{repo_name}/contents/README.md"
        
        # Setup headers
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.gh_token:
            headers["Authorization"] = f"token {self.gh_token}"
        
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
                logger.warning(f"Unexpected content encoding for {repo_name}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching README for {repo_name}: {str(e)}")
            return None

    def transform(self, example: dict) -> dict:
        repo_name = example['repo_name']
        readme_content = self.fetch_readme_content(repo_name)
        example['readme_exists'] = readme_content is not None
        example['readme'] = readme_content
        return example

    def create_readme_dataset(self, token: Optional[str] = None) -> None:
        """
        Create a DatasetDict containing README contents from multiple repositories.
        
        Args:
            repo_data (List[Dict]): List of dictionaries containing repo_name
            token (str, optional): GitHub personal access token
        
        Returns:
            DatasetDict: Dataset containing README contents
        """
        self.train_set = self.train_set.map(self.transform).filter(lambda x: x['readme_exists'])
        self.test_set = self.test_set.map(self.transform).filter(lambda x: x['readme_exists'])
        self.eval_set = self.eval_set.map(self.transform).filter(lambda x: x['readme_exists'])