import os

from .GetImg_search import Get_Image
# from .GetImg_reverse import Reverse_Image
from .Config import Path

from nonebot.plugin import PluginMetadata
from nonebot import get_driver
from nonebot.log import logger

__plugin_meta__ = PluginMetadata(
    name="EQAD Derpibooru图片搜索",
    description="从Derpibooru搜索图片",
    usage=".搜图 [tags]",
    config=None,
)

driver = get_driver()
@driver.on_startup
async def init_config():
    if not os.path.exists(Path + 'config.yml'):
        logger.info('未找到配置文件，正在创建...')
        InitialConfig_WithComments = """
# 填入你的Derpibooru API key (https://derpibooru.org/registrations/edit)，留空则使用默认配置
key: ''

# 是否启用内置tags
# 一行一个tag，格式为- <tag>
tags:
  enabled: true
  list:
    - safe
        """
        with open(Path + 'config.yml', 'w', encoding='utf8') as file:
            file.write(InitialConfig_WithComments)
        logger.info('配置文件创建成功')