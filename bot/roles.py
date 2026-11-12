import discord

FACE_SHAPE_ROLES: dict[str, int] = {
    "oval":      1570369164080586822,
    "round":     1570369839564857424,
    "square":    1570369865166884924,
    "triangle":  1570369904102871100,
    "oblong":    1570370162106830918,
    "rectangle": 1570370410099253255,
}

FAT_LEVEL_ROLES: dict[str, int] = {
    "stick":   1570370456983310366,
    "feather": 1570370492806995988,
    "skinny":  1570370511681355776,
    "fat":     1570370535400149003,
    "chunky":  1570370559294832732,
    "fatass":  1570370853504286783,
}

FACE_SHAPE_DISPLAY: dict[str, str] = {
    "oval":      "🥚 Egghead",
    "round":     "🥔 Potato",
    "square":    "🧀 Cheese Block",
    "triangle":  "🔻 Doritos",
    "oblong":    "🦒 Giraffe",
    "rectangle": "🐊 Crocodile",
}

ALL_MANAGED_ROLE_IDS: set[int] = set(
    list(FACE_SHAPE_ROLES.values()) + list(FAT_LEVEL_ROLES.values())
)


async def assign_face_shape_role(
    member: discord.Member,
    face_shape: str,
) -> discord.Role | None:
    """
    Remove any existing face-shape role from the member,
    then assign the new one. Returns the assigned Role or None.
    """
    guild = member.guild

    roles_to_remove = [
        role for role in member.roles
        if role.id in FACE_SHAPE_ROLES.values()
    ]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove, reason="Fat checker: removing old face-shape role")

    role_id = FACE_SHAPE_ROLES.get(face_shape)
    if not role_id:
        return None

    role = guild.get_role(role_id)
    if role is None:
        return None

    await member.add_roles(role, reason="Fat checker: assigning face-shape role")
    return role


async def assign_fat_level_role(
    member: discord.Member,
    fat_level: str,
) -> discord.Role | None:
    """
    Remove any existing fat-level role from the member,
    then assign the new one. Returns the assigned Role or None.
    """
    guild = member.guild

    roles_to_remove = [
        role for role in member.roles
        if role.id in FAT_LEVEL_ROLES.values()
    ]
    if roles_to_remove:
        await member.remove_roles(*roles_to_remove, reason="Fat checker: removing old fat-level role")

    role_id = FAT_LEVEL_ROLES.get(fat_level)
    if not role_id:
        return None

    role = guild.get_role(role_id)
    if role is None:
        return None

    await member.add_roles(role, reason="Fat checker: assigning fat-level role")
    return role
