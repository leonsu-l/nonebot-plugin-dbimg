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

# 定义一个异步函数，用于加载标签
    # 异步加载配置文件
async def load_tags():
    # 如果配置文件中的标签功能被启用
    config = await load_config()
        # 返回标签列表
    if config['tags']['enabled']:
        return config['tags']['list']
    return []


#NU1L_L
localizationZh = {
    'No_Proper_Picture':"没能找到合适的图片awa",
    "Internet_error":"网络错误",
    "Input_Error":"输入错误",
    "command":"搜图",
    "when_search":"正在搜索请稍候...",
    "Internal_Error":"内部错误"
}
precommand="safe,"

localization=localizationZh