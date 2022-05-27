# JScrapeON
JScrapeON is a web scraping tool that use JSON as its parser.


## Installation

Clone this [project](https://github.com/johnalbert-dot-py/JScrapeON/tree/master) and run:
```bash
pip install -r requirements.txt
```

## Usage

Use must first create a JSON parser configuration and place it under the `scrapes/` folder. You can look to an example below.

<img src="screenshots/JSON%20Parser%20Config%20-%20Example%20copy.png" alt="JSON Configuration Exmaple"/>


```python
# import libraries
from jscrapeon_parser.parse import JScrapeONParser
from jscrapeon_parser.config_parser import JsonConfig

# initialized the configuration with the name of the JSON Config file
json_config = JsonConfig(file_name="webscraper-e-commerce.json")
parser = JScrapeONParser(scrape_config=json_config).parse()
print(parser.stored_values)
```

The result must be something like this (since the scraped site change the result every loads).

<img src="https://github.com/johnalbert-dot-py/JScrapeON/blob/master/screenshots/Result%20-%20Example.png" alt="Example of Result">


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
