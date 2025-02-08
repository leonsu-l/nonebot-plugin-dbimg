'''
type:aaa,bbb,ccc;oc:aaa,bbb,ccc;
'''

from abc import ABC, abstractmethod

class parse(ABC):
    @abstractmethod
    def parse(self, data)->dict:
        pass