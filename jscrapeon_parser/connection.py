from dataclasses import dataclass
from typing import Optional, Union
from types import ModuleType
from requests.exceptions import RequestException
from requests import Session
import requests


@dataclass
class JScrapeONRequest:
    is_session: bool = False
    proxy: Optional[str] = None
    __session: Union[Session, ModuleType] = requests

    def __post_init__(self, *args, **kwargs):
        super(JScrapeONRequest, self).__init__()

        if self.is_session:
            self.__session = Session()
        else:
            self.__session = requests

    def make_post(self, **kwargs):
        return self.__session.post(**kwargs)

    def make_get(self, **kwargs):
        return self.__session.get(**kwargs)
