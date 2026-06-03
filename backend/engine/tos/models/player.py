from backend.engine.tos.models.role import Role
from backend.engine.tos.enums.status import Status


class Player:
    def __init__(self, pid, name, role: Role):
        self.id = pid
        self.name = name
        self.role = role
        self.alive = True
        self.defense = 0
        self.status = list()

    def add_status(self, status_type, source=None, data=None, expiry=None):
        status = Status(status_type, source, data, expiry)
        self.status.append(status)
        return status

    def has_status(self, status_type):
        for status in self.status:
            if status.is_type(status_type):
                return True
        return False

    def remove_status(self, status_type):
        for status in self.status:
            if status.is_type(status_type):
                self.status.remove(status)
                return

    def get_statuses(self, status_type):
        return [status for status in self.status if status.is_type(status_type)]

    def remove_expired_statuses(self, state):
        self.status = [status for status in self.status if not status.is_expired(state)]
