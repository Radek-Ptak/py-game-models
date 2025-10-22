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
                    defaults={
                        "description": guild_info.get("description", "")
                    })
            )

        player_obj, created = (
            Player.objects.get_or_create(
                nickname=player["nickname"],
                defaults={"email": player.get("email", ""),
                          "bio": player.get("bio", ""),
                          "race": race_obj,
                          "guild": guild_obj})
        )

        if not created:
            email = player.get("email")
            if email is not None:
                player_obj.email = email
            bio = player.get("bio")
            if bio is not None:
                player_obj.bio = bio
            if player.get("race") is not None:
                player_obj.race = race_obj
            if player.get("guild") is not None:
                player_obj.guild = guild_obj
            player_obj.save()

        skills = race_info.get("skills", [])

        for skill in skills:
            name = skill.get("name")
            bonus = skill.get("bonus")
            if not name or not bonus:
                continue
            skill_obj, created = Skill.objects.get_or_create(
                name=name,
                defaults={"bonus": bonus, "race": race_obj}
            )

            if not created:
                changed = False
                if skill_obj.bonus != bonus:
                    skill_obj.bonus = bonus
                    changed = True
                if changed:
                    skill_obj.save()


if __name__ == "__main__":
    main()
