from enum import Enum

class ClientCommandType(str, Enum):
    PING = "PING"
    JOIN_ROOM = "JOIN_ROOM"
    CHAT = "CHAT"
    READY = "READY"

class ServerEventType(str, Enum):
    PONG = "PONG"
    ERROR = "ERROR"
    ROOM_STATE = "ROOM_STATE"
    CHAT_MESSAGE = "CHAT_MESSAGE"
