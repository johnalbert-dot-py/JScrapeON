from abc import ABC, abstractmethod
from ast import Raise
from dataclasses import dataclass
from typing import List, Dict, Protocol, Optional
from .exceptions import ScrapeConfigError


class JscrapeOnConfigTest(ABC):
    """
    Protocol for the config test.
    """

    scrape_keys: List[str]
    required_keys: List[str]
    config: Dict

    @abstractmethod
    def test(self) -> Optional[Raise]:
        """
        Test the configuration.
        """


@dataclass
class ScrapeKeyTest(JscrapeOnConfigTest):

    scrape_keys: List[str]
    required_keys: List[str]
    config: Dict

    def test(self) -> Optional[Raise]:
        for key in self.scrape_keys:
            for rkey in self.required_keys:
                if rkey not in self.config[key]:
                    raise ScrapeConfigError(
                        "Key '{}' is missing in '{}'".format(rkey, key)
                    )


@dataclass
class ScrapeFieldKeyTest(JscrapeOnConfigTest):

    scrape_keys: List[str]
    required_keys: List[str]
    config: Dict

    def test(self) -> Optional[Raise]:
        for key in self.scrape_keys:
            to_scrape_fields = list(self.config[key]["scrape"].keys())
            if "html" not in to_scrape_fields and "json" not in to_scrape_fields:
                raise ScrapeConfigError(
                    "Scrape must have 'html' or 'json' in it".format(key)
                )


@dataclass
class ScrapeHTMLMustHaveKeyTest(JscrapeOnConfigTest):

    scrape_keys: List[str]
    required_keys: List[str]
    config: Dict

    def test(self) -> Optional[Raise]:
        for key in self.scrape_keys:
            to_scrape_fields = list(self.config[key]["scrape"]["html"].keys())
            missing_key = 0
            for required_key in self.required_keys:
                if required_key not in to_scrape_fields:
                    missing_key += 1
            if missing_key == len(self.required_keys):
                raise ScrapeConfigError(
                    f"Scrape must have '{', '.join(self.required_keys)}' in it"
                )


@dataclass
class ScrapeHTMLRequiredKeyTest(JscrapeOnConfigTest):

    scrape_keys: List[str]
    required_keys: List[str]
    config: Dict

    def test(self) -> Optional[Raise]:
        for key in self.scrape_keys:
            to_scrape_fields = list(self.config[key]["scrape"]["html"].keys())
            for required_key in self.required_keys:
                if required_key not in to_scrape_fields:
                    raise ScrapeConfigError(f"Scrape must have '{required_key}' in it")
