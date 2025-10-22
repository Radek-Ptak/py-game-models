import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for player in data:
        race_info = player.get("race")
        race_obj, _ = (
            Race.objects.get_or_create(
                name=race_info["name"],
                defaults={"description": race_info.get("description", "")})
        )

        guild_info = player.get("guild")

        if guild_info is None:
            guild_obj = None
        else:
            guild_obj, _ = (
                Guild.objects.get_or_create(
                    name=guild_info["name"],
                    defaults={"description": guild_info.get("description", "")}))

        player_obj, created = (
            Player.objects.get_or_create(
                nickname=player["nickname"],
                defaults={"email": player.get("email", ""),
                          "bio": player.get("bio", ""),
                          "race": race_obj,
                          "guild": guild_obj})
        )

        if not created:
            if "email" in player and player["email"] is not None:
                player_obj.email = player["email"]
            if "bio" in player and player["bio"] is not None:
                player_obj.bio = player["bio"]
            if "race" in player:
                player_obj.race = race_obj
            if "guild" in player:
                player_obj.guild = guild_obj
            player_obj.save()


if __name__ == "__main__":
    main()
