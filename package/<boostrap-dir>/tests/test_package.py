from unittest import TestCase

import <bootstrap-dir> as package


class PackageTestCase(TestCase):
    def test_package(self):
        assert package.NAME
        assert package.VERSION
        assert package.PY_VERSION
        assert package.AUTHOR
        assert package.AUTHOR_EMAIL
