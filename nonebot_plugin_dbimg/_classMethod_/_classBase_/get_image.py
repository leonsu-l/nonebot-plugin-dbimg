from abc import ABC, abstractmethod
class Image:
    def __init__(self, url: str,extra_page,id):
        self.url = url
        self.extra_page = extra_page
        self.id = id
class getImage(ABC):
    @abstractmethod
    async def get_image_list(self,filter_list)->dict|None:
        pass

    @abstractmethod
    def random_select_image(self,image_list)->Image|None:
        pass
