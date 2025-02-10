from .get_image import getImage
from abc import ABC, abstractmethod
#获取图片的装饰器类
class getImageDecorator(ABC):
	def __init__(self,getimage_method:getImage):
		self._getImage_metho=getimage_method
		pass