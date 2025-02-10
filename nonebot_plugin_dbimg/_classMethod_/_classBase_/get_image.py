from abc import ABC, abstractmethod

class Image:
    def __init__(self,
                 image_url: str,
                 image_name: str,
                 image_id: str,
                 tags: str,
                 sha512_hash: str,
                 artist: str,
                 imp: str
                 ):
        self.image_url = image_url  # 图片的url   file://
        self.image_name = image_name  # 图片的详情页
        self.image_id = image_id  # 图片的id
        self.tags = tags  # 图片的标签
        self.sha512_hash = sha512_hash  # 图片的哈希
        self.artist = artist  # 图片的作者
        self.imp = imp  # 图片发布的平台

class getImage(ABC):
    def __init__(self,imp):
        self.imp = imp
    @abstractmethod
    async def get_image_list(self,filter_list)->dict|None:
        pass

    @abstractmethod
    def random_select_image(self,image_list)->Image|None:
        pass
