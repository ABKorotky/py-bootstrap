__all__ = ("GenerateFilesProcessor",)

import logging
import typing as t
from functools import cached_property
from pathlib import Path

from .copy import CopyFilesProcessor

if t.TYPE_CHECKING:
    ...


logger = logging.getLogger(__name__)


class GenerateFilesProcessor(CopyFilesProcessor):
    _context: dict[str, str]

    @cached_property
    def _descriptor_file_name(self) -> str:
        return f"{self._source_path}.py"

    def set_context(self, value: dict[str, str]):
        self._context = value

    def generate_content_from_template(self, template: str) -> str:
        return template.format(**self._context)

    def check_file_for_processing(self, rel_path: "Path", file_name: str) -> bool:
        if file_name == self._descriptor_file_name:
            return False
        return super().check_file_for_processing(rel_path=rel_path, file_name=file_name)

    def process_file(self, rel_path: "Path", file_name: str):
        if file_name.endswith(".tmpl"):
            source_path = self._source_path.joinpath(rel_path, file_name)

            file_name = file_name.removesuffix(".tmpl")
            destination_path = self._destination_path.joinpath(rel_path, file_name)
            destination_path = Path(
                self.generate_content_from_template(
                    template=destination_path.as_posix()
                )
            )

            origin_content = source_path.read_text()
            prepared_content = self.generate_content_from_template(
                template=origin_content
            )
            if self._dry_run:
                self.log_dry_run_action(
                    action="generate file %r from %r template"
                    % (destination_path, source_path)
                )
            else:
                destination_path.write_text(prepared_content)
                logger.info(
                    "%r. generate file %r from %r template",
                    self,
                    destination_path,
                    source_path,
                )
        else:
            super().process_file(rel_path=rel_path, file_name=file_name)
