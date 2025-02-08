import random
from urllib.parse import quote
import urllib.request
from  ._classBase_.get_image import *
import json
class getImage_derpibooru(getImage):
    def __init__(self, api_key):
        self._api_key_ = api_key

    def convert_filter_list_to_string_pre(self, filter_list,pre="")->str:
        return_buffer=""
        for key, value in filter_list.items():
            if type(value) == str:
                return_buffer += pre+quote(value)+","
                continue
            if type(value) == dict:
                return_buffer += self.convert_filter_list_to_string_pre(value,pre=pre+quote(key)+":")
                continue
            raise Exception("bad filter_list type")
        return return_buffer

    def convert_filter_list_to_string(self, filter_list)->str:
        return self.convert_filter_list_to_string_pre(filter_list)[:-1]

    def get_image_list(self,filter_list)->dict|None:
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        url = f"https://derpibooru.org/api/v1/json/search/images?q={self.convert_filter_list_to_string(filter_list)}&sf=score&sd=desc&page=1&per_page=50&key={self._api_key_}"
        print(url)
        response = urllib.request.Request(url, headers=headers)
        try:
            response_ = urllib.request.urlopen(response)
            if response_.getcode() == 200:
                response_json = json.loads(response_.read().decode())
                if response_json.get("total") == 0:
                    return None
                return response_json
            raise Exception("bad response")
        except Exception as e:
            return None

    def random_select_image(self,image_list)->Image|None:
        if image_list['total'] == 0:
            return None
        image = random.choice(image_list['images'])
        if image['representations']['full'] is not None:
            image_url = image['representations']['large']
            image_id = image_url.split('/')[-2]
            img_source = f"https://derpibooru.org/images/{image_id}"
            return Image(image_url,img_source,image_id)
        else :
            return None
if __name__=="__main__":

    import parse
    parser=parse.NU1L_L_Parse()

    api_key = "DNYZd86ZNdATXKb2UjH0"
    derpibooru=getImage_derpibooru(api_key)
    a=derpibooru.get_image_list(parser.parse("😀"))
    if a is not None:
        #print(a)
        print(derpibooru.random_select_image(a))
    else:
        print("no image")
