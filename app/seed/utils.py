import os

from app.seed.consts import supported_clubs_lowered
from app.utils.utils import open_json_file

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_available_courts():
    tenis4u_courts = open_json_file(current_directory, "tenis4u_supported_courts.json")
    return [
        {
            "name": court["name"],
            "url": f'https://app.tenis4u.pl/#/court/{court["id"]}',
            "occupancyUrl": f'https://api.tenis4u.pl/occupancy/{court["id"]}',
            "img": court["miniature"],
        }
        for court in tenis4u_courts
        if court["name"].lower() in supported_clubs_lowered
    ]
