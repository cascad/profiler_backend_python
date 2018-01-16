import pathlib
import unittest

import pip
import pkg_resources


class TestRequirements(unittest.TestCase):
    def test_requirements(self):  # pylint: disable=no-self-use
        """Recursively confirm that requirements are available.

        This implementation is tested to be compatible with pip 9.0.1.
        """
        requirements_path = pathlib.Path(__file__).parents[1].joinpath('requirements.txt')
        requirements = pip.req.parse_requirements(str(requirements_path), session=pip.download.PipSession())
        requirements = [str(r.req) for r in requirements]
        pkg_resources.require(requirements)
