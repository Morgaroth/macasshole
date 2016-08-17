#!/usr/bin/env python3

import netifaces
from datetime import datetime
from netifaces import AF_LINK, AF_INET
from subprocess import run, PIPE
from time import sleep

CHECK_TIMEOUT = 2
WAIT_FOR_TURNING_OFF = 2
WAIT_FOR_TURNING_ON = 15

WIFI_CARD_MAC = 'f4:5c:89:92:d3:07'
THUNDERBOLT_CARD_MAC = '38:c9:86:2c:42:56'


def disable_wifi():
    result = run(['networksetup', '-setairportpower', 'en0', 'off'], stdout=PIPE, stderr=PIPE)
    print('%s: Turning off Wi-Fi end with code %d\n\tstdout: %s\n\tstderr: %s' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), result.returncode, repr(result.stdout), repr(result.stderr)))
    sleep(WAIT_FOR_TURNING_OFF)


def enable_wifi():
    result = run(['networksetup', '-setairportpower', 'en0', 'on'], stdout=PIPE, stderr=PIPE)
    print('%s: Turning on Wi-Fi end with code %d\n\tstdout: %s\n\tstderr: %s' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), result.returncode, repr(result.stdout), repr(result.stderr)))
    sleep(WAIT_FOR_TURNING_ON)


def checkThunderboltInternetConnected():
    return len([k for k, v in {i: netifaces.ifaddresses(i) for i in netifaces.interfaces()}.items() if
                AF_LINK in v and AF_INET in v and v[AF_LINK][0]['addr'] == THUNDERBOLT_CARD_MAC]) > 0


def checkWiFiEnabled():
    result = run(['networksetup', '-getairportpower', 'en0'], stdout=PIPE, stderr=PIPE)
    if result.stdout.startswith(b'Wi-Fi Power (en0): Off'):
        return False
    elif result.stdout.startswith(b'Wi-Fi Power (en0): On'):
        return True
    print('illegal result from get airport')
    print('%s: code %d\n\tstdout: %s\n\tstderr: %s' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), result.returncode, repr(result.stdout), repr(result.stderr)))


while True:
    sleep(CHECK_TIMEOUT)
    isThunderboltConnected = checkThunderboltInternetConnected()
    isWifiEnabled = checkWiFiEnabled()
    print('%s: Status is WiFi: %s, Thunderbolt: %s.' % (
        datetime.now().strftime('%H:%M:%S (%d/%b/2k%y)'), isWifiEnabled, isThunderboltConnected))

    if isThunderboltConnected and isWifiEnabled:
        disable_wifi()
    elif not isThunderboltConnected and not isWifiEnabled:
        enable_wifi()
