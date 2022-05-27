class ScrapeConfigError(Exception):
    """
    Error class for the configuration error on you JSON file.
    """


class ScrapingError(Exception):
    """
    Error class for an error in the main Scraping Function.

    It can be a error due to an invalid element on the page.

    """
