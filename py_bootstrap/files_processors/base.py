__all__ = ("BaseFilesProcessor",)

import logging
import typing as t

from py_bootstrap.base.operations import BaseOperation

if t.TYPE_CHECKING:
    from pathlib import Path


logger = logging.getLogger(__name__)


class BaseFilesProcessor(BaseOperation):
    _source_path: "Path"
    _destination_path: "Path"

    def set_source_path(self, source_path: "Path") -> None:
        self._source_path = source_path

    def set_destination_path(self, destination_path: "Path") -> None:
        self._destination_path = destination_path

    def run(self):
        for root_path, dirs_names, files_names in self._source_path.walk():
            logger.debug("%r. process %r source root.", self, root_path)
            rel_path = root_path.relative_to(self._source_path)

            for dir_name in dirs_names:
                if not self.check_directory_for_processing(
                    rel_path=rel_path, dir_name=dir_name
                ):
                    logger.debug(
                        "%r. directory %r/%r is skipped from processing.",
                        self,
                        rel_path,
                        dir_name,
                    )
                    continue

                try:
                    self.process_directory(rel_path=rel_path, dir_name=dir_name)
                except Exception as err:
                    logger.exception(
                        "%r. directory %r/%r processing failed: %r.",
                        self,
                        rel_path,
                        dir_name,
                        err,
                    )
                else:
                    logger.debug(
                        "%r. directory %r/%r is processed properly.",
                        self,
                        rel_path,
                        dir_name,
                    )

            for file_name in files_names:
                if not self.check_file_for_processing(
                    rel_path=rel_path, file_name=file_name
                ):
                    logger.debug(
                        "%r. file %r/%r is skipped from processing.",
                        self,
                        rel_path,
                        file_name,
                    )
                    continue

                try:
                    self.process_file(rel_path=rel_path, file_name=file_name)
                except Exception as err:
                    logger.exception(
                        "%r. file %r/%r processing failed: %r",
                        self,
                        rel_path,
                        file_name,
                        err,
                    )
                else:
                    logger.debug(
                        "%r. file %r/%r is processed properly.",
                        self,
                        rel_path,
                        file_name,
                    )

    def check_directory_for_processing(
        self, rel_path: "Path", dir_name: str
    ) -> bool:
        raise NotImplementedError(
            f"{self.__class__}.check_directory_for_generating"
        )

    def process_directory(self, rel_path: "Path", dir_name: str):
        raise NotImplementedError(f"{self.__class__}.process_directory")

    def check_file_for_processing(
        self, rel_path: "Path", file_name: str
    ) -> bool:
        raise NotImplementedError(f"{self.__class__}.check_file_for_processing")

    def process_file(self, rel_path: "Path", file_name: str) -> None:
        raise NotImplementedError(f"{self.__class__}.process_file")
