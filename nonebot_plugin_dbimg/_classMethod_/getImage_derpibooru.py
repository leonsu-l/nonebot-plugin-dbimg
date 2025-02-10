import random
from urllib.parse import quote
import aiohttp
from ._classBase_.get_image import getImage, Image

# 具体的derpibooru站获取图片的实现
class getImage_derpibooru(getImage):
	def __init__(self, _api_key_):
		super().__init__("derpibooru")
		self._http = None
		self._api_key_ = _api_key_

	# 初始化http会话
	def _init_http_event_loop(self):
		headers = {
			"Accept": "application/json",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
		}
		self._http = aiohttp.ClientSession(headers=headers)

	# 将输入的指令转化为可以参与搜索的字符串的具体实现
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

	#将输入的指令转化为可以参与搜索的字符串的修补函数
	def _convert_filter_list_to_string(self, filter_list) -> str:
		return self._convert_filter_list_to_string_pre(filter_list)[:-1]

	# 将平台返回的字符串转化为插件内部的数据格式
	@staticmethod
	def _convert_to_picture_list(picture_list: dict) -> list[Image]|None:
		# 检测数据是否合法,不合法的话就报错
		father_key_list = ["total", "images", "interactions"]
		for key in father_key_list:
			if key not in picture_list:
				raise Exception("bad list key")
		if picture_list["total"] == 0:
			return None
		image_list = []
		# 检查对象石里面是否有如下元素
		image_key_list = ["tags", "representations", "id", "name", "uploader", "name"]
		for i in picture_list["images"]:
			# 检测图片是否合格
			for image_key in image_key_list:
				if image_key not in i:
					raise Exception("bad image key")
			# 创建图片对象,类的原型在get_image.py
			image_list.append(Image(i["representations"]["full"],
			                        i["name"],
			                        i["id"],
			                        i["tags"],
			                        None,
			                        i["uploader"],
			                        i["name"]
			                        ))
		return image_list

	# 接口 获取图片列表
	async def get_image_list(self, filter_list) -> list[Image] | None:
		url = f"https://derpibooru.org/api/v1/json/search/images?q={self._convert_filter_list_to_string(filter_list)}&sf=score&sd=desc&page=1&per_page=50&key={self._api_key_}"
		self._init_http_event_loop()
		try:
			async with self._http as session:
				response = await session.get(url)
				if response.status != 200:
					raise Exception(response.status)
				response_json = await response.json()
				return self._convert_to_picture_list(response_json)
		except aiohttp.ClientResponseError as e:
			raise Exception("bad response")
		except aiohttp.ServerTimeoutError as e:
			raise Exception("Request timeout")

	# 接口 随机选择图片
	def random_select_image(self, image_list: list[Image]) -> Image | None:
		if len(image_list) == 0:
			return None
		image: Image = random.choice(image_list)
		return image