import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from utils import get_random_user_agent, save_to_csv

class EcommerceScraper:
    def __init__(self):
        self.base_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
        self.all_products = []
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
    def scrape_page(self, url):
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            
            print(f"Fetching : {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Failed to fetch {url} status: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = soup.find_all('div', class_='thumbnail')
            if not products:
                print("No products found on the page.")
                return False
            
            print(f"Found {len(products)} products on the page.")
            
            for product in products:
                product_data = {}
                
                name_tag = product.find('a', class_='title')
                product_data['name'] = name_tag.text.strip() if name_tag else 'No Name'
                
                price_tag = product.find('h4', class_='price')
                product_data['price'] = price_tag.text.strip() if price_tag else 'No Price'
                
                desc_tag = product.find('p', class_='description')
                product_data['description'] = desc_tag.text.strip() if desc_tag else 'No Description'
                
                rating_div = product.find('div', class_='ratings')
                if rating_div:
                    stars = len(rating_div.find_all('span', class_='glyphicon-star'))
                    product_data['rating'] = f"{stars}/5"
                else:
                    product_data['rating'] = 'No Rating'
                
                self.all_products.append(product_data)
                print(f"   Added: {product_data['name'][:30]}...")
            
            return True
        
        except Exception as e:
            print(f"An error occurred while scraping {url}: {e}")
            return False
        
    def handle_pagination(self):
        page_num = 1
        
        while True:
            if page_num == 1:
                current_url = self.base_url
            else:
                current_url = f"{self.base_url}?page={page_num}"
            
            success = self.scrape_page(current_url)
            
            if not success or len(self.all_products) >= 50:  
                break
            
            wait_time = random.uniform(2, 5)
            print(f" Waiting {wait_time:.1f} seconds before next page...")
            time.sleep(wait_time)
            
            page_num += 1
        
        print(f"\n Finished! Scraped {len(self.all_products)} products total")
    
    def run(self):
        print(" STARTING E-COMMERCE SCRAPER")
        
        self.handle_pagination()
        
        if self.all_products:
            # Save to different formats
            df = pd.DataFrame(self.all_products)
        
            df.to_csv('output/products.csv', index=False, encoding='utf-8')
            print(" Saved to 'output/products.csv'")
        
            df.to_json('output/products.json', orient='records', indent=2)
            print(" Saved to 'output/products.json'")
            
            print("\n SAMPLE DATA:")
            print(df.head(3).to_string())
        else:
            print(" No data was scraped")


if __name__ == "__main__":
    scraper = EcommerceScraper()
    scraper.run()