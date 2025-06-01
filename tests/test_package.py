import typing as t
from unittest import TestCase

import py_bootstrap as package

if t.TYPE_CHECKING:
    ...


class PackageTestCase(TestCase):
    def test_package(self):
        assert package.NAME
        assert package.VERSION
        assert package.PY_VERSION
        assert package.AUTHOR
        assert package.AUTHOR_EMAIL
