from ast import Raise
from optparse import Option
from typing import List, Dict, Protocol, Tuple, Optional
from config.constant import PROJECT_ROOT
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, abstractproperty
from config.exceptions import ScrapeConfigError
from config.config_test import (
    JscrapeOnConfigTest,
    ScrapeKeyTest,
    ScrapeFieldKeyTest,
    ScrapeHTMLMustHaveKeyTest,
    ScrapeHTMLRequiredKeyTest,
)
import json


class Config(ABC):

    config: Dict = field(default_factory=dict)
    required_keys: List[str] = ["url", "method", "scrape"]
    must_have_scrape_data_keys: List[str] = ["html", "json"]

    must_have_html_keys: List[str] = ["selector", "id", "name", "class", "tag", "xpath"]
    required_html_keys: List[str] = ["get", "count"]

    @abstractmethod
    def set_config_file(self) -> Dict:
        """
        Return the configuration as Dictionary in a file.
        """

    @abstractmethod
    def get_configuration_keys(self) -> Dict:
        """
        Return the config keys such as:

            as_session = bool |

            proxy = str
        """

    @abstractmethod
    def get_scrape_keys(self) -> List[str]:
        """
        Return the scrape keys where the scraping start.
        """

    @abstractmethod
    def test_all_config(self) -> None:
        """
        Test all config that are provided.
        """


@dataclass
class JsonConfig(Config):

    debug: bool = False
    config_tester: List[JscrapeOnConfigTest] = field(default_factory=list)
    config: Dict = field(default_factory=dict)

    def set_config_file(self, file_name):
        json_data = ""
        configuration_directory = PROJECT_ROOT + "scrapes/"
        file_path = configuration_directory + file_name

        with open(file_path) as json_file:
            json_data = json.load(json_file)
            self.config = json_data
            json_file.close()
        self.test_all_config()
        return json_data

    def test_all_config(self):
        self.config_tester = [
            ScrapeKeyTest(self.get_scrape_keys(), self.required_keys, self.config),
            ScrapeFieldKeyTest(
                self.get_scrape_keys(), self.must_have_scrape_data_keys, self.config
            ),
            ScrapeHTMLMustHaveKeyTest(
                self.get_scrape_keys(), self.must_have_html_keys, self.config
            ),
            ScrapeHTMLRequiredKeyTest(
                self.get_scrape_keys(), self.required_html_keys, self.config
            ),
        ]
        for config in self.config_tester:
            config.test()

    def get_configuration_keys(self):

        as_session = False
        if "as_session" in self.config:
            as_session = self.config["as_session"]

        proxy = ""
        if "proxy" in self.config:
            proxy = self.config["proxy"]

        return {"as_session": as_session, "proxy": proxy}

    def get_scrape_keys(self):
        all_keys = list(self.config.keys())
        all_keys.remove("as_session")
        all_keys.remove("proxy")
        return all_keys


# a = JsonConfig()
# a.set_config_file("webscraper-e-commerce.json")
