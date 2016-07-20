#!/usr/bin/env python3

from datetime import datetime
from subprocess import run, PIPE
from time import sleep

try:
    from setproctitle import setproctitle
except ImportError:
    print("SetProcTitle module not found, may You should install it? 'pip install setproctitle'")
    raise

CONNECT_TIMEOUT = '1'
CHECK_TIMEOUT = 5
WAIT_FOR_TURNING_OFF = 2
WAIT_FOR_TURNING_ON = 15

code = 0
debug = False

setproctitle('Wi-Fii Checker')


def execute_req():
    cmd = ['curl', '-X', 'HEAD', '--connect-timeout', CONNECT_TIMEOUT, 'www.wp.pl']
    if debug:
        print(' '.join(cmd))
    return run(cmd, stdout=PIPE, stderr=PIPE)


while True:
    while code == 0:
        result = execute_req()
        code = result.returncode
        if debug:
            print('Checking internet connection end with code %d and stdout %s and stderr %s' % (
                code, repr(result.stdout), repr(result.stderr)))
        sleep(CHECK_TIMEOUT)

    result = run(['networksetup', '-setairportpower', 'en0', 'off'], stdout=PIPE, stderr=PIPE)
    print('%s: Turning off Wi-Fi end with code %d\n\tstdout: %s\n\tstderr: %s' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), result.returncode, repr(result.stdout), repr(result.stderr)))
    sleep(WAIT_FOR_TURNING_OFF)
    result = run(['networksetup', '-setairportpower', 'en0', 'on'], stdout=PIPE, stderr=PIPE)
    print('%s: Turning on Wi-Fi end with code %d\n\tstdout: %s\n\tstderr: %s' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), result.returncode, repr(result.stdout), repr(result.stderr)))
    sleep(WAIT_FOR_TURNING_ON)
    code = execute_req().returncode
