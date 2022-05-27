from jscrapeon_parser.parse import JScrapeONParser
from jscrapeon_parser.connection import JScrapeONRequest
from jscrapeon_parser.config_parser import JsonConfig


json_config = JsonConfig()
json_config.set_config_file("webscraper-e-commerce.json")
parser_connection = JScrapeONRequest(is_session=json_config.config["as_session"])
parser = JScrapeONParser(session=parser_connection, scrape_config=json_config)
result = parser.parse()
