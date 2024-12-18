import os

from app.db.config import client
from app.utils.utils import open_json_file

current_directory = os.path.dirname(os.path.abspath(__file__))

favorite_list = [
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


def get_available_courts(all_courts):

    favorite_list_lowered = [el.lower() for el in favorite_list]

    return [
        {
            "name": court["name"],
            "url": f'https://app.tenis4u.pl/#/court/{court["id"]}',
            "occupancyUrl": f'https://api.tenis4u.pl/occupancy/{court["id"]}',
            "img": court["miniature"],
        }
        for court in all_courts
        if court["name"].lower() in favorite_list_lowered
    ]


def run_get_tenis4u_available_courts():
    tenis4u_courts = open_json_file(current_directory, "tenis4u_supported_courts.json")
    available_courts = get_available_courts(tenis4u_courts)
    all_tennis_courts_collection = client["tennis"]["clubs"]
    all_tennis_courts_collection.drop()
    all_tennis_courts_collection.insert_many(available_courts)


run_get_tenis4u_available_courts()
