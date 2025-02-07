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

Reverse_Image = on_command("图搜图", priority=10, block=True)

@Reverse_Image.handle()
async def handle_reverse_image(bot: Bot, event: MessageEvent):
    img_url = event.get_message()
    img_url = img_url[0].data['url']
    logger.info(f"用户输入图片链接: {img_url}")
    
    url = "https://derpibooru.org/api/v1/json/search/images"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Content-Type": "application/json"
    }
    data = {
        "url": img_url
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_content = response.text
    data = json.loads(json_content)
    logger.info(data)
    if data['images']:
        image = data['images'][0]
        image_id = image['id']
        image_url = f"https://derpibooru.org/images/{image_id}"
        image_score = image['score']
        image_upvotes = image['upvotes']
        image_downvotes = image['downvotes']
        image_faves = image['faves']
        image_tags = image['tags']
        image_tag_string = ""
        for tag in image_tags:
            image_tag_string += f"{tag}, "
        image_tag_string = image_tag_string[:-2]
        image_string = f"图片链接: {image_url}\n评分: {image_score}\n赞: {image_upvotes}\n踩: {image_downvotes}\n收藏: {image_faves}\n标签: {image_tag_string}"
        await Reverse_Image.finish(image_string)
    else:
        await Reverse_Image.finish("未找到相关图片")