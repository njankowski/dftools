from inspect import currentframe
from os.path import basename, splitext
from sys import stderr, stdout


verbose = False


def set_verbose(enabled):
    global verbose
    verbose = enabled


def vprint(message, file=stdout):
    if verbose:
        caller_current_frame = currentframe()
        caller_path = caller_current_frame.f_back.f_code.co_filename
        caller_fuction_name = caller_current_frame.f_back.f_code.co_name
        caller_filename = splitext(basename(caller_path))[0]
        print(f'{caller_filename}:{caller_fuction_name}: {message}', file=file)
