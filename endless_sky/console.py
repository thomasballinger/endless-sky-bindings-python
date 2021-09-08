import code                                                  
import readline
import rlcompleter
import threading


from .loader import FilesystemPrepared
from . import bindings as es




def run_with_console(path=None, *, resources=None, config=None, extra_args=None):
    if extra_args is None: extra_args = []

    ns = {'es': es}
    readline.set_completer(rlcompleter.Completer(ns).complete) 
    readline.parse_and_bind("tab: complete")                     

    game_has_quit = False
    repl_is_running = False

    def repl():
        nonlocal repl_is_running
        repl_is_running = True
        code.InteractiveConsole(ns).interact(banner='Welcome to the sky!')
        if not game_has_quit:
            print("you've exited the Interactive Console, but Endless Sky is still running")
            print("TODO make it quit when this happens")
        repl_is_running = False

    console_thread = threading.Thread(target=repl)
    console_thread.start()


    # Run game stuff on the main thread
    with FilesystemPrepared(path=path, resources=resources, config=config) as (resources_path, config_path):
        args = [
            'progname', # This is just to take up the first argument
            '--no-catch',  # don't catch thrown runtime_error
            '--resources', resources_path,
            '--config', config_path,
        ] + extra_args
        print("running main() with args:", args)
        if '--resources' in extra_args:
            print('WARNING: extra --resource flag will override')
        if '--config' in extra_args:
            print('WARNING: extra --resource flag will override')

        try:
            es.main_no_GIL(args)
        except RuntimeError as e:
            print('caught exception thrown while running main():', e)
        finally:
            game_has_quit = True
            if (repl_is_running):
                print('main() finished running.')
                print("You can keep interacting with es objects if you want.")
                print("Don't call main() again, that'd be weird.")
                print("")
                print('Type exit() and hit enter or use ctrl-D (mac/linux only maybe?) to delete temporary files and quit.')
            console_thread.join()
    print('Finished cleanup')
