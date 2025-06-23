__all__ = ("CopyFilesProcessor",)

import logging
import typing as t
from shutil import copyfile

from .base import BaseFilesProcessor

if t.TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class CopyFilesProcessor(BaseFilesProcessor):
    excluded_directories: list[str] = ["__pycache__", ".DS_Store"]
    excluded_file_extensions: list[str] = [".pyc", ".pyd", ".pyo"]

    def check_directory_for_processing(
        self, rel_path: "Path", dir_name: str
    ) -> bool:
        return dir_name not in self.excluded_directories

    def process_directory(self, rel_path: "Path", dir_name: str):
        path = self._destination_path.joinpath(rel_path, dir_name)
        path.mkdir(parents=True, exist_ok=True)

    def check_file_for_processing(
        self, rel_path: "Path", file_name: str
    ) -> bool:
        for excluded_dir in self.excluded_directories:
            if excluded_dir in rel_path.as_posix():
                return False

        for file_extension in self.excluded_file_extensions:
            if file_name.endswith(file_extension):
                return False

        return True

    def process_file(self, rel_path: "Path", file_name: str):
        source_path = self._source_path.joinpath(rel_path, file_name)
        destination_path = self._destination_path.joinpath(rel_path, file_name)
        copyfile(source_path, destination_path)
