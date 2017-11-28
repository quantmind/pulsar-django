# -*- coding: utf-8 -
import sys

import pulsar
from pulsar.api import Setting, Config
from pulsar.apps.wsgi import WSGIServer

from pulse.wsgi import Wsgi

from django.core.management.base import (
    BaseCommand, CommandError, OutputWrapper, handle_default_options
)


class PulseAppName(Setting):
    section = "Django Pulse"
    app = "pulse"
    name = "pulse_app_name"
    flags = ["--pulse-app-name"]
    default = 'django_pulsar'
    desc = """\
        Name for the django pulse application
        """


class Command(BaseCommand):
    help = "Starts a fully-functional Web server using pulsar."
    args = 'pulse --help for usage'

    def handle(self, *args, **options):
        if args:
            raise CommandError('pulse --help for usage')
        app_name = options.get('pulse_app_name')
        callable = Wsgi()
        if options.pop('dryrun', False) is True:  # used for testing
            return callable
        # callable.setup()
        cfg = Config(apps=['socket', 'pulse'],
                     server_software=pulsar.SERVER_SOFTWARE,
                     **options)
        server = WSGIServer(callable=callable, name=app_name, cfg=cfg,
                            parse_console=False)
        callable.cfg = server.cfg
        server.start()

    def get_version(self):
        return pulsar.__version__

    def create_parser(self, prog_name, subcommand):
        parser = super().create_parser(prog_name, subcommand)
        cfg = Config(apps=['socket', 'pulse'],
                     exclude=['debug'],
                     description=self.help,
                     version=self.get_version())
        return cfg.add_to_parser(parser)

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        handle_default_options(options)
        try:
            self.execute(**options.__dict__)
        except Exception as e:
            if options.traceback or not isinstance(e, CommandError):
                raise

            # self.stderr is not guaranteed to be set here
            stderr = getattr(self, 'stderr',
                             OutputWrapper(sys.stderr, self.style.ERROR))
            stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)
