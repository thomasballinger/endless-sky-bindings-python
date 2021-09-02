import argparse
import sys
import os

#import endless_sky_bindings as es

parser = argparse.ArgumentParser(
    prog='python -m mymodule',
    description="Endless Sky utilities, backed by "
)
parser.add_argument('--version', action='store_true')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help',
                                   dest="subcommand")
parse_parser = subparsers.add_parser('parse')
parse_parser.add_argument("file")

subparsers.add_parser('version')

args = parser.parse_args()
print(args)
if args.version or args.subcommand == "version":
    print('this is a version es.version')
    sys.exit(0)


# For Endless Sky data to be loaded, the following is required:
# - an installed version of the game or a checkout of the Endless Sky repo
#   (use --no-resources to ignore this)
# - a config location, where save games and plugins are stored.
#   (use --no-

# When parsing we need to choose a resources directory.
# This is loaded before any plugins.
# You can parse data with this first, you can use an empty resources dir,
# or you can substitude your own resources dir.
# The plugins folder in that resources dir will be searched for plugins.
# If you're trying to ignore those plugins, maybe you want to copy the
# other parts of the resources folder somewhere else.
# Next, you need to choose a config directory.
# This will also be searched for plugins.
# This is also used to specify saved games.
# The default values should be
# - find all possible installations of Endless Sky, choose one to use
# - use those installed resources and plugins
# - 

if args.subcommand == 'parse':
    print("let's parse a file or resources directory:", args.file)
    if not os.path.exists(args.file):
        print("that file does not exist!")
        exit(1)
    if os.path.isdir(args.file):
        print("parse this as a resources directory")
    
