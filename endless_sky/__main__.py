import argparse
import json
import os
import sys
import logging
from pathlib import Path

import endless_sky
import endless_sky.bindings as es
from endless_sky.parser import parse_ships
from endless_sky.console import run_with_console

class StoreDefaultConfig(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, nargs=0, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        saves = es.saves_directory()  # creating saves directory as a side effect
        path = str(Path(saves).parent)
        setattr(namespace, self.dest, path)

def exists(path):
    if path is None:
        return path
    if not os.path.exists(path):
        raise ValueError("path %r does not exist" % path)

def add_file_resources_and_config(parser):
    """Require some resources arg, default config to None, and default file to None."""
    parser.add_argument("file", nargs="?", type=exists, help="data file or directory of data files")

    resources_group = parser.add_mutually_exclusive_group(required=True)
    resources_group.add_argument('--resources')
    resources_group.add_argument('--empty-resources', action='store_const', const=None, dest='resources')

    config_group = parser.add_mutually_exclusive_group(required=False)
    # empty config is the default
    config_group.add_argument("--config", default=None)
    config_group.add_argument("--empty-config", action='store_const', const=None, dest='config')
    config_group.add_argument("--default-config", action=StoreDefaultConfig, dest='config')

parser = argparse.ArgumentParser(
    prog='python -m mymodule',
    description="Endless Sky utilities powered by the actual Endless Sky codebase."
)
parser.add_argument('--version', action='store_true')
parser.add_argument('--verbose', '-v', action='count', default=0)
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help',
                                   dest="subcommand")

load_parser = subparsers.add_parser('load', description='Parse a set of data files')
add_file_resources_and_config(load_parser)
load_parser.add_argument("--format", default='pretty', help='pretty (default), json, or dict')

run_parser = subparsers.add_parser('run', description='Run endless sky (this pip-installed one) passing arguments through')
add_file_resources_and_config(run_parser)
run_parser.add_argument('rest', nargs=argparse.REMAINDER, help='extra command line args to pass to main()')

subparsers.add_parser('version')

args = parser.parse_args()

# Default logging level is WARN, -v kicks it to INFO, -vv to DEBUG
level = [logging.WARN, logging.INFO, logging.DEBUG][args.verbose]
logging.basicConfig(stream=sys.stdout, level=level)

if args.version or args.subcommand == "version":
    print(endless_sky.version)
    sys.exit(0)
elif not args.version and not args.subcommand:
    parser.print_help()
    sys.exit(0)

# when analyzing a save game file, you can only use installed plugins
# if the saved game is in the save game folder!

# we need to be able to discover existing endless sky installations
# or have an endless sky repo manually specified.
# Later, have a script that does a zip download somewhere https://github.com/endless-sky/endless-sky/archive/1873fd9ee9a9ad6a4fd210fe03f8d5a6fc7abc25.zip
# Where do these get downloaded to? I dunno, where does nltk put its datasets?
# Maybe a .endless-sky-python-assets in home? Maybe use config dir logic?

# TODO add autodiscovery of resources
# --find-resources
# --use-cached-resources (or maybe this is the default?)

if args.subcommand == 'load':
# TODO use add_mutually_exclusive_group() for this instead
    if args.file is not None and not os.path.exists(args.file):
        logging.error("that file does not exist!")
        exit(1)
    if args.file:
        logging.info("parsing custom file or directory %s", args.file)
        logging.info("by symlinking to it from a temporary config directory")
    output = parse_ships(
        args.file,
        format=args.format,
        resources=args.resources,
        config=args.config
    )
    print(output)

elif args.subcommand == 'run':
    run_with_console(
        args.file,
        resources=args.resources,
        config=args.config,
        extra_args=args.rest
    )
    # TODO the GIL should probably only be held and only released between
    # frames but for now it's never held so a world of race conditions are likely
