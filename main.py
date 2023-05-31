import asyncio

from core.Config import GlobalConfig
from core.EventListener import LeagueEventListener
from core.IndexPage import IndexPage
from core.PluginLoader import load_plugins

GlobalConfig.set_config_file_path(r"C:\Users\23518\Desktop\LeagueWizard-master\config.txt")


async def main():
    load_plugins("plugins")
    cli_task = asyncio.create_task(IndexPage.loop())
    asyncio.create_task(LeagueEventListener.start())

    await cli_task


asyncio.run(main())
