from pydantic import BaseModel, field_validator
import yaml

from nonebot.log import logger

Path = 'nonebot_plugin_dbimg/'
'''
class Config(BaseModel):
    api_key: str = ''
    internal_tags: bool = True
    internal_tags_list: list = []
'''
async def load_config():
    with open(Path + 'config.yml', 'r', encoding='utf8') as file:
        config = file.read()
    return yaml.safe_load(config)

async def load_key():
    config = await load_config()
    return config['key']

async def load_tags():
    config = await load_config()
    if config['tags']['enabled']:
        return config['tags']['list']
    return []