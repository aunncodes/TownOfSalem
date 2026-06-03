from enum import Enum, auto


class StatusType(Enum):
    FRAMED = auto()
    JAILED = auto()
    ALERT = auto()
    ROLEBLOCKED = auto()
    WATCHED = auto()


def single_night_status(state, data):
    return True


class Status:
    def __init__(self, status_type, source=None, data=None, expiry=None):
        self.type = status_type
        self.source = source
        self.data = data or {}
        self.expiry = expiry or single_night_status

    def is_expired(self, state):
        return self.expiry(state, self.data)

    def is_type(self, status_type):
        return self.type == status_type
