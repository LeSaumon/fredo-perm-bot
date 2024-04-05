import nextcord
from loguru import logger

from config import DISCORD_TOKEN, GUILD_ID
from bot import bot


async def get_members_by_roles(requested_roles: list[str]) -> list[nextcord.Member]:
    guild = await bot.fetch_guild(GUILD_ID)
    members = [
        {
            member.name: {
                "roles": [
                    role.name for role in member.roles if role.name != "@everyone"
                ],
                "member": member,
            }
        }
        for member in await guild.fetch_members().flatten()
    ]
    requested_members = []
    for member in members:
        roles = list(member.values())[0]["roles"]
        member_object = list(member.values())[0]["member"]
        if set(requested_roles).issubset(set(roles)):
            requested_members.append(member_object)
    return requested_members


@bot.event
async def on_ready():
    logger.info("fredo is ready!")


@bot.event
async def on_guild_channel_create(channel: nextcord.abc.GuildChannel):
    if "🔒" in channel.name:
        guild = await bot.fetch_guild(GUILD_ID)
        requested_roles = [
            role.name
            for role in channel.changed_roles
            if role.name != "@everyone" and role.name != "Fredo"
        ]
        logger.info(requested_roles)
        members_to_add = await get_members_by_roles(requested_roles)
        logger.info(members_to_add)
        for role_name in requested_roles:
            role = nextcord.utils.get(guild.roles, name=role_name)
            if role.name == "Fredo":
                logger.info(
                    "Fredo role cannot be removed from a channel (and shouldn't be)"
                )
            else:
                await channel.set_permissions(role, overwrite=None)
                logger.info(f"Removing {role.name} from channel {channel.name}")
        for member in members_to_add:
            overwrite = nextcord.PermissionOverwrite()
            overwrite.view_channel = True
            await channel.set_permissions(target=member, overwrite=overwrite)
            logger.info(
                f"Added {member.name} permision to {overwrite} to channel {channel.name}"
            )


def main():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
