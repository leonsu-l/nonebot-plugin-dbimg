import requests
import json
import re

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.log import logger

import random

from nonebot import get_driver
driver = get_driver()
driver.config.command_start = {".", "。"}

from .Config import load_key, load_tags

headers = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

async def is_valid_input(plaintext):
    invalid_chars = ["&", "@", "#", "$", "%", "^", "*", "(", ")", "=", "[", "]", "{", "}", "\\", "|", ";", "\"", "<", ">", "/", "?"]
    pattern = f'[{"".join(map(re.escape, invalid_chars))}]'
    # logger.info(f"非法符号：{pattern}")
    if re.search(pattern, plaintext):
        return False  
    else:
        return True

async def handle_input_tags(plaintext):
    tags_plaintext = plaintext[3:].strip()
    if not await is_valid_input(tags_plaintext):
        await Get_Image.finish("检测到非法字符，请重新搜索")
    tags = re.split(" ,|, | ，|， |，|,", tags_plaintext)
    
    str_tags = ""

    if not tags:
        logger.info("处理后无tags")
    else:
        # logger.info(f"用户输入tags处理完毕: {tags}")
        str_tags = "%2C".join(tags)

    return str_tags

async def handle_internal_tags():
    tags = await load_tags()

    str_tags = ""

    if not tags:
        logger.info("未启用/添加内置tags")
    else:
        logger.info(f"内置tags: {tags}")
        str_tags = "%2C".join(tags)

    return str_tags

async def image_select(json_content):
    data = json.loads(json_content)

    if data['total'] == 0:
        await Get_Image.finish("没有找到相关图片")

    image = random.choice(data['images'])
    
    if image['representations']['full'] is not None:
        img_url = image['representations']['large']
        logger.success(f"获取到图片链接: {img_url}")
        return img_url
    else:
        await Get_Image.finish("没有找到相关图片")
    
    
Get_Image = on_command("搜图", priority=10, block=True)

@Get_Image.handle()
async def handle_Get_Image(bot: Bot, event: MessageEvent):
    plaintext = event.get_plaintext().strip()
    
    internal_tags = await handle_internal_tags()
    input_tags = await handle_input_tags(plaintext=plaintext)

    if not input_tags:
        await Get_Image.finish("请输入tags后再搜索")

    q = f"{(f'{internal_tags}%2C') if internal_tags else ''}{input_tags}"
    q_log = q.replace("%2C", ",")
    logger.info(f"正在搜索{q_log}的图片")

    api_key = await load_key()
    if api_key:
        key = f'&key={api_key}'
    else:
        logger.info("未使用key")
        key = ''
    
    url = f"https://derpibooru.org/api/v1/json/search/images?q={q}&sf=score&sd=desc&page=1&per_page=50{key}"
    
    if len(url) > 1020:
        await Get_Image.finish("搜索内容过长，请减少标签数量")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(str(e))
        await Get_Image.finish(f"网络异常，请联系bot管理员")
        
    json_content = response.text

    img_url = await image_select(json_content=json_content)
    
    if img_url:
        at = MessageSegment.at(event.user_id)
        image = MessageSegment.image(img_url)
        img_id = img_url.split('/')[-2]
        img_source = f"https://derpibooru.org/images/{img_id}"
        await bot.send(event, at + image + img_source)
    else:
        await Get_Image.finish("没有找到相关图片")
