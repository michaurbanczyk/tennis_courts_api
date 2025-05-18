def get_players_passwords(tournament_players: list[dict], match_players: list[str]):
    return list(
        map(
            lambda player: player["password"],
            filter(lambda player: player["name"] in match_players, tournament_players),
        )
    )
