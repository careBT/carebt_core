from carebt.version import __version__


class TestVersion:

    def test_version(self):
        assert __version__ != ''
