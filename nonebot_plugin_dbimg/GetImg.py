from exceptiongroup import catch
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.log import logger
from nonebot import get_driver
from .Config import load_key, load_tags
from .Config import localization
from .Config import precommand
from .Config import config
from ._classMethod_._classBase_.get_image import *
from ._classMethod_._classBase_.parse import *

import unicodedata
import re

import asyncio


def _init_user_():
	pass


def _init_system_():
	global driver
	global Get_Image
	global image_method
	global parse_method

	driver = get_driver()
	driver.config.command_start = {".", "。"}
	Get_Image = on_command(localization["command"], priority=10, block=True)

def chinese_punctuation_to_english(s):
	punctuation_map = {
		'。': '.',
		'，': ',',
		'；': ';',
	}
	return ''.join(punctuation_map.get(c, c) for c in s)


def preprecess(data) -> str:
	data = chinese_punctuation_to_english(data)
	print(data)
	return data


def get_purl_cmd(str_) -> str:
	str_ = preprecess(str_)
	cmd = str_.strip()[len(localization["command"]) + 1:].strip()
	return cmd


def bot_send(bot: Bot, event: MessageEvent, message):
	at = MessageSegment.at(event.user_id)
	return bot.send(event, at + message)


async def handle_get_image(bot: Bot, event: MessageEvent, image_method: getImage, filter_parse: parse):
	await bot_send(bot, event, localization["when_search"])
	plaintext = precommand + get_purl_cmd(event.get_plaintext())
	try:
		input_tags = filter_parse.parse(plaintext)
	except Exception as e:
		logger.error(f"<UNK>{plaintext}")
		await bot_send(bot, event, localization["Input_Error"])
		return
	if input_tags is None:
		await bot_send(bot, event, localization["Input_Error"])
		return
	try:
		image_list = await image_method.get_image_list(input_tags)
	except Exception("bad response") as e:
		await bot_send(bot, event, localization["Internal_Error"])
		logger.error(f"{e}")
		return
	except Exception("Request timeout") as e:
		await bot_send(bot, event, localization["Internal_Error"])
		logger.error(f"{e}")
		return
	if image_list is None:
		await bot_send(bot, event, localization["No_Proper_Picture"])
		return
	random_image = image_method.random_select_image(image_list)
	try:
		print(random_image.url)
		if config["fail_times"]:
			fail_times=config["fail_times"]
		else:
			fail_times=1
		image=MessageSegment.image(random_image.url)
		while fail_times > 0:
			image = MessageSegment.image(random_image.url)
			if not image:
				fail_times -= 1
			else:
				break
		if fail_times > 0:
			await bot_send(bot, event,image + "id" + random_image.id)
		else:
			await bot_send(bot, event,"图片下载失败,id"+random_image.url)
	except Exception as e:
		logger.error(e)
		await bot_send(bot, event, localization["Internal_Error"])
		return


_init_system_()

from ._classMethod_.getImage_derpibooru import *
from ._classMethod_.parse import *

api_key = load_key()
image_method = getImage_derpibooru(api_key)
parse_method = NU1L_L_Parse()


@Get_Image.handle()
async def _main_(bot: Bot, event: MessageEvent):
	if asyncio.get_event_loop().is_running():
		asyncio.create_task(handle_get_image(bot, event, image_method, parse_method))
	else:
		asyncio.run(handle_get_image(bot, event, image_method, parse_method))
