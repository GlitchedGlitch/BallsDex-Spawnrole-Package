"""
this is where magic happens :3
"""

import logging

import discord
from discord.ui import TextDisplay

from ballsdex.packages.countryballs.countryball import BallSpawnView
from bd_models.models import GuildConfig

log = logging.getLogger("ballsdex.packages.spawnrole")

_original_build = BallSpawnView.build


async def _fetch_spawn_role(guild_id: int) -> int | None:
    config = await GuildConfig.objects.filter(guild_id=guild_id).select_related("spawn_role_data").afirst()
    return config.spawn_role_data.role_id if config and hasattr(config, "spawn_role_data") and config.spawn_role_data else None


async def _patched_build(self, spawn_message: str, file_name: str, guild_id: int | None = None) -> None:
    # Call original build first
    await _original_build(self, spawn_message, file_name, guild_id)

    # If no guild context, nothing to do
    if guild_id is None:
        return

    # Fetch configured spawn role
    spawn_role_id = await _fetch_spawn_role(guild_id)
    if not spawn_role_id:
        return

    # Try to resolve the role object to check if it still exists
    guild = self.bot.get_guild(guild_id)
    role = guild.get_role(spawn_role_id) if guild else None

    # Build the mention text
    if role:
        mention_text = f"<@&{role.id}>"
    else:
        mention_text = f"<@&{spawn_role_id}>"

    mention_display = TextDisplay(mention_text)
    self._children.insert(1, mention_display)

def apply():
    BallSpawnView.build = _patched_build
    log.info("Patched BallSpawnView.build for spawn role mentions (LayoutView v3)")


def revert():
    BallSpawnView.build = _original_build
    log.info("Reverted BallSpawnView.build patch")
