import requests
import os
import base64


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None or not str(value).strip():
        raise ValueError(
            f"Environment variable '{name}' is not set or is empty")
    return str(value).strip()


class CatalogConfig:
    def __init__(self, organization: str, repository: str, token: str):
        self.__token__ = token
        self.organization = organization
        self.repository = repository

    @classmethod
    def from_env(cls):
        token = get_env_var('GITHUB_ACCESS_TOKEN')
        organization = get_env_var('GITHUB_ORG')
        repository = get_env_var('GITHUB_REPO')
        return cls(organization, repository, token)


class GithubCatalog:
    def __init__(self):
        self.__config__ = CatalogConfig.from_env()

    @property
    def headers(self):
        return {
            'Authorization': f'token {self.__config__.__token__}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def list_files(self, folder: str) -> dict:
        """
        List all files in the specified folder of the GitHub repository.
        """
        url = f'https://api.github.com/repos/{self.__config__.organization}/{self.__config__.repository}/contents/{folder}'
        print(url)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        files = [file['name']
                 for file in response.json() if file['type'] == 'file']
        return {"files": files}

    def file_exists(self, file_name: str, folder: str) -> bool:
        """
        Check if a file exists in the specified folder of the GitHub repository.
        """
        url = f'https://api.github.com/repos/{self.__config__.organization}/{self.__config__.repository}/contents/{folder}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        files = [file['name']
                 for file in response.json() if file['type'] == 'file']
        return file_name in files

    def upload_file(self, file_content: bytes, file_name: str, folder: str):
        """
        Upload a file to the specified folder in the GitHub repository.
        """
        file_path = os.path.join(folder, file_name)
        url = f'https://api.github.com/repos/{self.__config__.organization}/{self.__config__.repository}/contents/{file_path}'
        data = {
            'message': f'{folder}: Add {file_name}',
            'content': base64.b64encode(file_content).decode()
        }
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()

    def download_file(self, file_path: str) -> bytes:
        """
        Download a file from the specified path in the GitHub repository.
        """
        url = f'https://raw.githubusercontent.com/{self.__config__.organization}/{self.__config__.repository}/master/{file_path}'
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    
    def delete_file(self, file_name: str, folder: str):
        """
        Delete a file from the specified folder in the GitHub repository.
        """
        file_path = os.path.join(folder, file_name)
        url = f'https://api.github.com/repos/{self.__config__.organization}/{self.__config__.repository}/contents/{file_path}'
        
        # First, we need to get the SHA of the file to delete it
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        sha = response.json()['sha']
        
        data = {
            'message': f'{folder}: Delete {file_name}',
            'sha': sha
        }
        
        response = requests.delete(url, headers=self.headers, json=data)
        response.raise_for_status()
        
