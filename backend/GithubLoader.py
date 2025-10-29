import subprocess
from langchain.document_loaders import GitLoader
import tempfile
import shutil

def file_filter(file_path):
    ignore_filepaths = ["package-lock.json"]
    for ignore_filepath in ignore_filepaths:
        if ignore_filepath in file_path:
            return False
    return True


class GithubLoader:
    def __init__(self):
        """
        this class is responsible for loading in a github repository
        """

    def load(self, url: str):
        tmp_path = tempfile.mkdtemp()
        try:
            subprocess.run(["git", "clone", url, tmp_path], check=True)
            # Let GitLoader detect the default branch; do not pass branch to avoid GitPython dependency
            loader = GitLoader(repo_path=tmp_path,
                               file_filter=file_filter)
            documents = loader.load()
        finally:
            # Clean up the temporary directory
            shutil.rmtree(tmp_path)
        return documents


