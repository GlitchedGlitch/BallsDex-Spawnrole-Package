from __future__ import annotations
from typing import TYPE_CHECKING
from .cog import SpawnRoleCog
from . import spawn_patch

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot

async def setup(bot: "BallsDexBot") -> None:
    spawn_patch.apply()
    await bot.add_cog(SpawnRoleCog(bot))

async def teardown(bot: "BallsDexBot") -> None:
    spawn_patch.revert()
    cog = bot.cogs.get("SpawnRoleCog")
    if cog is not None and hasattr(cog, "_detach"):
        cog._detach()
