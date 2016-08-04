"""Tests the pulse Command."""
import unittest

from pulsar.apps import wsgi
from pulse.management.commands.pulse import Command


class pulseCommandTest(unittest.TestCase):

    def test_pulse(self):
        cmnd = Command()
        hnd = cmnd.handle(dryrun=True)
        self.assertTrue(isinstance(hnd, wsgi.LazyWsgi))
