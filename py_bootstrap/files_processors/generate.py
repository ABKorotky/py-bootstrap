__all__ = ("GenerateFilesProcessor",)

import logging
import typing as t
from pathlib import Path

from .copy import CopyFilesProcessor

if t.TYPE_CHECKING:
    ...


logger = logging.getLogger(__name__)


class GenerateFilesProcessor(CopyFilesProcessor):
    _context: dict[str, str]
    _entry_point_file_name: str

    def set_context(self, value: dict[str, str]):
        self._context = value

    def set_entry_point_file_name(self, value: str):
        self._entry_point_file_name = value

    def generate_content_from_template(self, template: str) -> str:
        return template.format(**self._context)

    def process_directory(self, rel_path: "Path", dir_name: str):
        path = self._destination_path.joinpath(rel_path, dir_name)
        path = Path(
            self.generate_content_from_template(template=path.as_posix())
        )
        path.mkdir(parents=True, exist_ok=True)

    def check_file_for_processing(
        self, rel_path: "Path", file_name: str
    ) -> bool:
        if file_name == self._entry_point_file_name:
            return False
        return super().check_file_for_processing(
            rel_path=rel_path, file_name=file_name
        )

    def process_file(self, rel_path: "Path", file_name: str):
        if file_name.endswith(".tmpl"):
            source_path = self._source_path.joinpath(rel_path, file_name)

            file_name = file_name.removesuffix(".tmpl")
            destination_path = self._destination_path.joinpath(
                rel_path, file_name
            )
            destination_path = Path(
                self.generate_content_from_template(
                    template=destination_path.as_posix()
                )
            )

            origin_content = source_path.read_text()
            prepared_content = self.generate_content_from_template(
                template=origin_content
            )
            destination_path.write_text(prepared_content)
        else:
            super().process_file(rel_path=rel_path, file_name=file_name)
