from exceptiongroup import catch
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.log import logger
from nonebot import get_driver
from .Config import load_key, load_tags
from .Config import localization
from .Config import precommand

from ._classMethod_._classBase_.get_image import *
from ._classMethod_._classBase_.parse import *

driver = get_driver()
driver.config.command_start = {".", "。"}
Get_Image = on_command(localization["command"], priority=10, block=True)


def get_purl_cmd(str_) -> str:
	return str_.strip()[len(localization["command"]) + 1:].strip()


async def bot_send(bot: Bot, event: MessageEvent, message):
	at = MessageSegment.at(event.user_id)
	await bot.send(event, at + message)


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
	image_list = image_method.get_image_list(input_tags)

	if image_list is None:
		await bot_send(bot, event, localization["No_Proper_Picture"])
		return
	random_image = image_method.random_select_image(image_list)
	try:
		image = MessageSegment.image(random_image.url)
		await bot_send(bot, event, image + random_image.extra_page)
	except:
		await bot_send(bot, event, localization["Internal_Error"])
		return


from ._classMethod_.getImage_derpibooru import *
from ._classMethod_.parse import *


@Get_Image.handle()
async def _main_(bot: Bot, event: MessageEvent):
	api_key =await load_key()
	image_method = getImage_derpibooru(api_key)
	parse_method = NU1L_L_Parse()
	await handle_get_image(bot, event, image_method, parse_method)
