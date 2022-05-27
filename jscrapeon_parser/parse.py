from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import ModuleType
from typing import Any, List, Dict, Tuple, Optional, Union
from webbrowser import get
from bs4 import BeautifulSoup
import json

from jscrapeon_parser.connection import JScrapeONRequest
from jscrapeon_parser.config_parser import Config
from config.exceptions import ScrapeConfigError, ScrapingError
from config.constant import GET_KEY_VALUE
from requests import Response


class Parser(ABC):
    @abstractmethod
    def parse(self, *args, **kwargs) -> List[Dict]:
        pass


class ScrapeOnInterface(ABC):
    """
    An interface for scraping a specific scrape configuration.
    """

    config: Config
    request: JScrapeONRequest

    @abstractmethod
    def scrape(self) -> Tuple[bool, str]:
        """
        Will return a Tuple with boolean as a status and a string as the parsed result.
        (True, "succes") or (False, "failed")
        """


@dataclass
class ScrapeOn(ScrapeOnInterface):
    """
    A class for scraping a specific scrape configuration.
    """

    config: Dict
    request: JScrapeONRequest

    def value_parser(
        self, text: Union[List, Any], getter: str, count: int = 0
    ) -> Union[List, str]:
        if not count:
            if getter == "text":
                return [t.text for t in text]
            elif getter == "value":
                return [t.value for t in text]
            else:
                try:
                    return [t[getter] for t in text]
                except ScrapingError:
                    raise ScrapingError(
                        f"Invalid Attriute or Getter for scraper: {getter}"
                    )

        elif count > 1:
            text = text[:count]
            if getter == "text":
                return [t.text for t in text]
            elif getter == "value":
                return [t.value for t in text]
            else:
                try:
                    return [t[getter] for t in text]
                except ScrapingError:
                    raise ScrapingError(
                        f"Invalid Attriute or Getter for scraper: {getter}"
                    )
        else:
            if getter == "text":
                return text[0].text
            elif getter == "value":
                return text[0].value
            else:
                try:
                    return text[0][getter]
                except ScrapingError:
                    raise ScrapingError(
                        f"Invalid Attriute or Getter for scraper: {getter}"
                    )

    def html_parser(self, parser: BeautifulSoup) -> Union[List, str]:
        html_config = self.config["scrape"]["html"]
        select_parser = parser.select
        parser_config = ""

        if GET_KEY_VALUE("tag", html_config):
            parser_config = html_config["tag"]

        if GET_KEY_VALUE("id", html_config):
            parser_config += f"[id='{html_config['id']}']"

        if GET_KEY_VALUE("name", html_config):
            parser_config += f"[name='{html_config['name']}']"

        if GET_KEY_VALUE("class", html_config):
            parser_config += f"[class='{html_config['class']}']"

        result = select_parser(parser_config)
        if len(result) == 0:
            raise ScrapingError(
                f"No element found with the Scrape Selector: {parser_config}"
            )
        else:
            scrape_result = self.value_parser(
                result, html_config["get"], html_config["count"]
            )
            return scrape_result

    def scrape(self) -> Tuple[bool, Union[List, str]]:
        source_request: Union[Response, Any] = ""
        if self.config["method"] == "GET":
            source_request = self.request.make_get(
                url=self.config["url"],
                data=self.config["data"],
                params=self.config["params"],
                headers=self.config["headers"],
            )
        elif self.config["method"] == "POST":
            source_request = self.request.make_post(
                url=self.config["url"],
                data=self.config["data"],
                params=self.config["params"],
                headers=self.config["headers"],
            )
        else:
            raise ScrapingError(f"Invalid method: {self.config['method']}")

        if "json" in self.config["scrape"]:
            source_request = source_request.json()  # type: ignore
        else:
            source_request = source_request.text  # type: ignore

        if "show_source" in self.config:
            if self.config["show_source"]:
                print(source_request)

        if "html" in self.config["scrape"]:
            source_parser = BeautifulSoup(source_request, "html.parser")
            return (True, self.html_parser(source_parser))
        else:
            source_parser = source_request

        return (False, "Method not implemented")


@dataclass
class JScrapeONParser(Parser):
    """
    Default parser for JSrapeON.
    """

    session: JScrapeONRequest
    scrape_config: Config
    stored_values: List[Dict] = field(default_factory=list)

    def parse(self):
        """
        Parse the keys on configuration where the scraping starts.
        """
        scrape_keys = self.scrape_config.get_scrape_keys()
        for key in scrape_keys:
            result = ScrapeOn(self.scrape_config.config[key], self.session).scrape()
            if result[0]:
                self.stored_values.append({"name": key, "value": result[1]})
            else:
                raise ScrapingError("Scraping failed on key: " + key)
