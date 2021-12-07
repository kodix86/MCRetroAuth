#!/bin/python3

from proxy import Proxy
from solo import Solo
from exit import ExitStatus

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mode", help="Select the server mode to use, solo, proxy, or register.", required=True)
parser.add_argument("-u", "--username", help="Username to register")
parser.add_argument("-p", "--password", help="Password to register")

args = parser.parse_args()

exit_val = 0

if args.mode == "solo":
    solo = Solo("3rd Party MC auth server")
    print("Running in solo mode! (currently unimplemented)")

    exit_val = solo.server_handle()

elif args.mode == "register":
    solo = Solo("3rd Party MC auth server")
    print("Registering a user for solo mode!")

    if args.username is not None and args.password is not None:
        exit_val = solo.register(args.username, args.password)
    else:
        print("Tried to register a user, but did not supply either a username, or a password?")
        exit_val = ExitStatus.invalid_params

elif args.mode == "login":
    solo = Solo("3rd Party MC auth server")
    print("Attempting login locally! (Test Purposes Only!)")

    if args.username is not None and args.password is not None:
        exit_val = solo.login(args.username, args.password)
    else:
        print("Tried to login a user, but did not supply either a username, or a password?")
        exit_val = ExitStatus.invalid_params

elif args.mode == "proxy":
    proxy = Proxy("Proxy for official Mojang auth servers, with added features")
    print("Running as a proxy! (currently unimplemented)")
    exit_val = ExitStatus.unimplemented

else:
    print("Unknown mode \"" + args.mode + "\" try solo or proxy.")
    exit_val = ExitStatus.invalid_params

print(exit_val)
exit(exit_val.value)
