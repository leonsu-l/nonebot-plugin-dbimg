from ._classBase_.get_image_decorator import getImageDecorator
from ._classBase_.get_image import getImage, Image

class cache_decorator_getImage(getImageDecorator):
	def __init__(self, getimage_method: getImage):
		super().__init__(getimage_method)

	def get_image_list(self, filter_list) -> dict | None:
		pass

	def random_select_image(self, image_list) -> Image | None:
		pass
