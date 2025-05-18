def get_players_passwords(tournament_players: list[dict], match_players: list[str], key: str):
    return list(
        map(
            lambda player: player["password"],
            filter(lambda player: player[key] in match_players, tournament_players),
        )
    )
