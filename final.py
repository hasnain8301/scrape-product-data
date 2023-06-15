from openpyxl import load_workbook
import grequests
from bs4 import BeautifulSoup
from write_data import add_data_to_excel

product_list = []
# SCRPE PRODUCT DATA FORM EVERY PRODUCT PAGE
def scrape_product_page(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    # GET THE PRODUCT DATA 
    product_name = soup.find('span', attrs={'class': 'product-info__product-title text text--secondary css-e2pi8n-textBase-textLarge'}).get_text()
    description = soup.find('p', attrs={'class': 'extra-details__text-content css-vj8cjy-fontSmoothingStyles-bodyBaseStyles-bodySmallStyles'}).get_text()
    price = soup.find('meta', attrs={'property': 'og:price:amount'}).get('content')
    image_url = soup.find_all('link', attrs={'itemprop': 'image'})[1:]
    images = []
    for image in image_url:
        images.append(image.get('href'))
    image_url = images
    product_list.append([product_name, description,f"${price}", str(image_url)])


# TAKE A LIST OF URL OF EACH PRODUCT PAGE AS PARAMETER
def get_product_info(url_list):
    requests = (grequests.get(f'https://www.minted.com/product/original-paintings/{url}/gold-boreal-forest?color=A&g&shape=') for url in url_list)
    responses = grequests.map(requests)
    for num,response in enumerate(responses):
        if response is not None and response.status_code == 200:
            print(f'{num} - status_code: ', response.status_code)
            # CALL FUNCTION TO SCRAP EACH PRODUCT PAGE
            scrape_product_page(response)
    # CALL FUNCTION TO SAVE DATA IN EXCEL SHEET
    add_data_to_excel(product_list, 'product.xlsx', 'Sheet1')
    product_list.clear()