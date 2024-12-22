from enum import StrEnum


class FetchingStatus(StrEnum):
    STARTED = "Started"
    SUCCESS = "Success"
    ERROR = "Error"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"
    PREPARED = "Prepared"


SUPPORTED_CLUBS = [
    "Rudawa Tennis Club",
    "Sport Factory Park",
    "Fame Sport Club",
    "TCC Sport Resort KORTY",
    "Magic Sports",
    "Klub Sportowy Grzegórzecki - Flex Wysłouchów 34",
    "PANTA REI",
    "Korty Białoprądnicka",
    "Park Wola Sodowa",
    "Kort w Pękowicach",
    "KSU Grzegórzecki",
]

supported_clubs_lowered = [el.lower() for el in SUPPORTED_CLUBS]
