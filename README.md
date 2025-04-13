
# TokopediaScrapper

TokopediaScrapper is a Python-based web scraping tool designed to retrieve product data from [Tokopedia](https:///tokopedia.com) using a specified keyword. It allows you to extract all matching products and fetch detailed product descriptions, with options to save the results into a CSV file.

## Features
- Scrape all products matching a keyword.
- Retrieve product details including description.
- Save results to a CSV file.
- Pagination support via max_pages parameter.

## Requirements
Required libraries (install via `pip install -r requirements.txt`):

## Usage
For Usage see `main.py` for Example

### Class Intialization
```python
from TokopediaScrapper import TokopediaScrapper

scraper = TokopediaScrapper(keyword="laptop", csvFile="laptops.csv", type='a')
```
- `keyword` : The search term to query Tokopedia.
- `csvFile` : Path to save CSV file
- `type` : Type to store file, a =  Append

### Fetch All products
```python
scraper.fetch_all_products(max_pages=10)  # max_pages is optional
```
- max_pages (optional): Maximum number of pages to scrape. If not provided, the scraper will attempt to retrieve all available pages.

## ⚠️ Caution

> **Important:** This project is not affiliated with or endorsed by Tokopedia. Use at your own risk and for lawful, ethical purposes only. We do not take responsibility for any misuse of this code.
