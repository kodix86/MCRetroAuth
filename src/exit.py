#!/usr/bin/false

from enum import Enum


class ExitStatus(Enum):
    unimplemented = 255
    success = 0
    invalid_params = 1
    invalid_username = 2
    auth_failure = 3
