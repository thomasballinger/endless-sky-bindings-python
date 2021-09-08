import argparse
import json
import os
import sys

import endless_sky
from endless_sky.parser import parse_ships
from endless_sky.console import run_with_console

parser = argparse.ArgumentParser(
    prog='python -m mymodule',
    description="Endless Sky utilities powered by the actual Endless Sky codebase."
)
parser.add_argument('--version', action='store_true')
parser.add_argument('--verbose', action='store_true')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help',
                                   dest="subcommand")

parse_parser = subparsers.add_parser('parse', description='Parse a set of data files')
parse_parser.add_argument("file", nargs="?", help="data file or directory of data files")
parse_parser.add_argument("--resources", default=None)
parse_parser.add_argument("--empty-resources", action="store_true")
parse_parser.add_argument("--config", required=False, default=None)
parse_parser.add_argument("--format", default='pretty', help='pretty (default), json, or dict')

run_parser = subparsers.add_parser('run', description='Run endless sky (this pip-installed one) passing arguments through')
run_parser.add_argument("file", nargs="?", help="data file or directory of data files")
run_parser.add_argument("--resources", default=None)
run_parser.add_argument("--empty-resources", action="store_true")
run_parser.add_argument("--config", required=False, default=None)
run_parser.add_argument('rest', nargs=argparse.REMAINDER)

subparsers.add_parser('version')

args = parser.parse_args()
if args.verbose:
    print(args)
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

# TODO use add_mutually_exclusive_group() for this instead
# TODO add autodiscovery of resources
# --find-resources
# --use-cached-resources (or maybe this is the default?)
def check_resources(args):
    """Check that --resources and --empty-resources args were used sensibly"""
    if not args.resources and not args.empty_resources:
        print("Either specify --resources PATH or use --empty-resources to use an empty resources directory")
        sys.exit(1)
    if args.resources and args.empty_resources:
        print("Don't specify both --resources PATH and --empty-resources")
    return args.resources

if args.subcommand == 'parse':
    if args.file is not None and not os.path.exists(args.file):
        print("that file does not exist!")
        exit(1)
    if args.file:
        print("parsing custom file or directory:", args.file)
        print("by symlinking to it from a temporary config directory")
    output = parse_ships(
        args.file,
        format=args.format,
        resources=check_resources(args),
        config=args.config
    )
    print(output)

elif args.subcommand == 'run':
    resources = check_resources(args)
    run_with_console(
        args.file,
        resources=check_resources(args),
        config=args.config,
        extra_args=args.rest
    )
    # TODO the GIL should probably only be held and only released between
    # frames but for now it's never held so a world of race conditions are likely
