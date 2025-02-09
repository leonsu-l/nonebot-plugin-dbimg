import random
from urllib.parse import quote
import aiohttp
from ._classBase_.get_image import *
import json


class getImage_derpibooru(getImage):
	def __init__(self, api_key):
		self._api_key_ = api_key

	def _init_http_event_loop(self):
		headers = {
			"Accept": "application/json",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
		}
		self._http = aiohttp.ClientSession(headers=headers)

	async def _fetch(self, session, url):
		async with session.get(url) as response:
			return await response.text()

	def _convert_filter_list_to_string_pre(self, filter_list, pre="") -> str:
		return_buffer = ""
		for key, value in filter_list.items():
			if type(value) == str:
				return_buffer += pre + quote(value) + ","
				continue
			if type(value) == dict:
				return_buffer += self._convert_filter_list_to_string_pre(value, pre=pre + quote(key) + ":")
				continue
			raise Exception("bad filter_list type")
		return return_buffer

	def _convert_filter_list_to_string(self, filter_list) -> str:
		return self._convert_filter_list_to_string_pre(filter_list)[:-1]

	async def get_image_list(self, filter_list) -> dict | None:
		url = f"https://derpibooru.org/api/v1/json/search/images?q={self._convert_filter_list_to_string(filter_list)}&sf=score&sd=desc&page=1&per_page=50&key={self._api_key_}"
		self._init_http_event_loop()
		try:
			async with self._http as session:
				data = await self._fetch(session, url)
				response_json = json.loads(data)
				if response_json.get("total") == 0:
					return None
				return response_json
		except aiohttp.ClientResponseError as e:
			raise Exception("bad response")
		except aiohttp.ServerTimeoutError as e:
			raise Exception("Request timeout")
		except Exception as e:
			return None

	def random_select_image(self, image_list) -> Image | None:
		if image_list['total'] == 0:
			return None
		image = random.choice(image_list['images'])
		if image['representations']['full'] is not None:
			image_url = image['representations']['large']
			image_id = image_url.split('/')[-2]
			img_source = f"https://derpibooru.org/images/{image_id}"
			return Image(image_url, img_source, image_id)
		else:
			return None


if __name__ == "__main__":

	import parse

	parser = parse.NU1L_L_Parse()

	api_key = ""
	derpibooru = getImage_derpibooru(api_key)
	a = derpibooru.get_image_list(parser.parse("😀"))
	if a is not None:
		print(derpibooru.random_select_image(a))
	else:
		print("no image")
