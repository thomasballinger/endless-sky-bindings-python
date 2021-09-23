import code
import sys
import logging
import threading

try:
    import readline
    import rlcompleter
except ImportError:
    # Windows doens't have readline
    readline = None
    pass

def p(*args):
    print(*args, file=sys.stderr)

from .loader import FilesystemPrepared
from . import bindings as es

banner = """Welcome to the sky!
Try dir(es) or use dir on a class like dir(es.GameData) to see what you can do.
You can get a reference you your ship with:
your_ship = es.PlayerInfo.CurrentPlayer().Ships()[0]
You can get a dictionary of all ship templates with:
ships = dict(es.GameData.Ships())
"""

def run_with_console(path=None, *, resources=None, config=None, extra_args=None):
    if extra_args is None: extra_args = []

    ns = {'es': es}
    if readline:
        readline.set_completer(rlcompleter.Completer(ns).complete)
        readline.parse_and_bind("tab: complete")

    game_has_quit = False
    repl_is_running = False

    def repl():
        nonlocal repl_is_running
        repl_is_running = True
        code.InteractiveConsole(ns).interact(banner=banner)
        if not game_has_quit:
            p("you've exited the Interactive Console, but Endless Sky is still running")
            p("TODO make it quit when this happens")
        repl_is_running = False

    console_thread = threading.Thread(target=repl)

    # Run game stuff on the main thread
    with FilesystemPrepared(path=path, resources=resources, config=config) as (resources_path, config_path):
        args = [
            'progname', # This is just to take up the first argument
            '--no-catch',  # don't catch thrown runtime_error
            '--resources', resources_path,
            '--config', config_path,
        ] + extra_args
        logging.warning("running main() with args: %s", args)
        if '--resources' in extra_args:
            logging.warning('WARNING: extra --resource flag will override')
        if '--config' in extra_args:
            logging.warning('WARNING: extra --resource flag will override')

        console_thread.start()
        try:
            es.main_no_GIL(args)
        except RuntimeError as e:
            logging.warning('caught exception (in C++ code) while running main(): %s', e)
        finally:
            game_has_quit = True
            if (repl_is_running):
                p('main() finished running.')
                p("You can keep interacting with es objects if you want.")
                p("Don't call main() again, that'd be weird.")
                p("")
                p('Type exit() and hit enter or use ctrl-D (mac/linux only maybe?) to delete temporary files and quit.')
            console_thread.join()
    p('finished cleanup')
    logging.info('finished cleanup')
