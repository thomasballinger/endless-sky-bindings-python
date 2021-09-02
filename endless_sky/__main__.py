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
#   (use --no-resources to ignore this and use a blank one)
# - a config location, where save games and plugins are stored.
#   (use --use-installed-plugins to include installed plugins, by default
#   a temp config directory will be used.

# when analyzing a save game file, you can only use installed plugins
# if the saved game is in the save game folder!

# when previewing an individual plugin file, use an assumed name of zzzz or something?

# we need to be able to discover existing endless sky installations
# or have an endless sky repo manually specified.
# Later, have a script that does a zip download somewhere https://github.com/endless-sky/endless-sky/archive/1873fd9ee9a9ad6a4fd210fe03f8d5a6fc7abc25.zip
# Where do these get downloaded to? I dunno, where does nltk put its datasets?
# Maybe a .endless-sky-python-assets in home? Maybe use config dir logic?

if args.subcommand == 'parse':
    print("let's parse a file or resources directory:", args.file)
    if not os.path.exists(args.file):
        print("that file does not exist!")
        exit(1)
    if os.path.isdir(args.file):
        print("parse this as a resources directory")
    
