from abc import ABC, abstractmethod
import requests
import os
import base64
from .log import LoggerFactory
from enum import Enum

SERVICE_GRAPH_FOLDER = 'service_graphs'
NETWORK_FUNCTION_FOLDER = 'network_functions'


logger = LoggerFactory.get_logger(__name__)


class Catalog(ABC):
    @abstractmethod
    def list_files(self, folder: str) -> dict:  # type: ignore
        """
        List all files in the specified folder of the catalog.
        """
        pass

    @abstractmethod
    def file_exists(self, file_name: str, folder: str) -> bool:  # type: ignore
        """
        Check if a file exists in the specified folder of the catalog.
        """
        pass

    @abstractmethod
    def upload_file(self, file_content: bytes, file_name: str, folder: str) -> None:
        """
        Upload a file to the specified folder in the catalog.
        """
        pass

    @abstractmethod
    def download_file(self, file_path: str) -> bytes:  # type: ignore
        """
        Download a file from the specified path in the catalog.
        """
        pass

    @abstractmethod
    def delete_file(self, file_name: str, folder: str) -> None:
        """
        Delete a file from the specified folder in the catalog.
        """
        pass


def get_catalog() -> Catalog:
    """
    Factory function to get an instance of the Catalog.
    This can be extended to return different catalog implementations.
    """
    try:
        return GithubCatalog()

    except Exception as e:
        logger.warning(f"Failed to initialize Github catalog: {e}")
        logger.warning("Falling back to local catalog")
    try:
        base_path = "/tmp/d6g/catalog/"
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        return LocalCatalog(base_path)
    except Exception as e:
        logger.error(f"Failed to initialize local catalog: {e}")
        raise RuntimeError("No catalog implementation available") from e

class GithubConfig:
    def __init__(self, organization: str, repository: str, token: str):
        self.__token__ = token
        self.organization = organization
        self.repository = repository

    @staticmethod
    def get_env_var(name: str) -> str:
        value = os.getenv(name)
        if value is None or not str(value).strip():
            logger.error(
                f"Environment variable '{name}' is not set or is empty")
            raise ValueError(
                f"Environment variable '{name}' is not set or is empty")
        return str(value).strip()

    @classmethod
    def from_env(cls):
        token = cls.get_env_var('GITHUB_ACCESS_TOKEN')
        organization = cls.get_env_var('GITHUB_ORG')
        repository = cls.get_env_var('GITHUB_REPO')
        return cls(organization, repository, token)


class GithubCatalog(Catalog):
    def __init__(self):
        self.__config__ = GithubConfig.from_env()
        self.headers = {
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

class LocalCatalog(Catalog):
    def __init__(self, base_path: str):
        self.base_path = base_path
        sgPath = os.path.join(base_path, SERVICE_GRAPH_FOLDER)
        nfPath = os.path.join(base_path, NETWORK_FUNCTION_FOLDER)
        if not os.path.exists(sgPath):
            os.makedirs(sgPath)
        if not os.path.exists(nfPath):
            os.makedirs(nfPath)
            
    def list_files(self, folder: str) -> dict:
        full_path = os.path.join(self.base_path, folder)
        files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
        return {"files": files}

    def file_exists(self, file_name: str, folder: str) -> bool:
        full_path = os.path.join(self.base_path, folder, file_name)
        return os.path.exists(full_path)

    def upload_file(self, file_content: bytes, file_name: str, folder: str):
        full_path = os.path.join(self.base_path, folder, file_name)
        with open(full_path, 'wb') as f:
            f.write(file_content)

    def download_file(self, file_path: str) -> bytes:
        full_path = os.path.join(self.base_path, file_path)
        with open(full_path, 'rb') as f:
            return f.read()

    def delete_file(self, file_name: str, folder: str):
        full_path = os.path.join(self.base_path, folder, file_name)
        if os.path.exists(full_path):
            os.remove(full_path)
            
class FileType(str, Enum):
    SERVICE_GRAPH = 'service_graph'
    NETWORK_FUNCTION = 'network_function'