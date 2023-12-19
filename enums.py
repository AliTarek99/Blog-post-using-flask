from enum import Enum


class State(Enum):
    duplicate = 1
    short_pass = 2
    valid = 3
    notfound = -1
