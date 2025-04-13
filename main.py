from TokopediaScrapper import TokopediaScrapper
import time

keyword = "handphone"
toped = TokopediaScrapper(keyword,f"Tokopedia_Product_{keyword}_{time.strftime('%Y-%m_%d-%H-%M-%S', time.gmtime())}.csv")

product = toped.fetch_all_products(30)