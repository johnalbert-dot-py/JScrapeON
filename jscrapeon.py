from jscrapeon_parser.parse import JScrapeONParser
from jscrapeon_parser.connection import JScrapeONRequest
from jscrapeon_parser.config_parser import JsonConfig


json_config = JsonConfig(file_name="webscraper-e-commerce.json")
parser = JScrapeONParser(scrape_config=json_config)
parser.parse()
print(parser.stored_values)
