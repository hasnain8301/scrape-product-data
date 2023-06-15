import grequests
from bs4 import BeautifulSoup
from final import get_product_info

url_list = []
# SCRAPE THE URL OF EACH ITEM ON PAGINATION PAGES
def scrape_page(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    anchor_tags = soup.find_all('a', attrs={'class': 'css-1mskf89-textBase-textMedium-textEmphasis-productNameStyles'})
    
    # ITERATE anchor_tags TO GET SKU-KEY
    for i,anchor in enumerate(anchor_tags):
        product_url = anchor.get('href')
        split_string = product_url.split("/")
        data = split_string[3]
        url_list.append(data)

# TAKE LIST OF PAGENATION URL's AND USE G-REQUEST
def scrape_data(urls):
    requests = (grequests.get(url) for url in urls)
    responses = grequests.map(requests)
    # ITERATE THROUGH RESPONSES
    for response in responses:
        if response is not None and response.status_code == 200:
            # CALL SCRAPE PAGE FUNCTION
            scrape_page(response)
        get_product_info(url_list)
        url_list.clear()

# BASE URL FOR PAGINATION
base_url = 'https://www.minted.com/shop-direct-from-artist'
page_param = 'page'
start_page = 1
end_page = 5

# CREATE A LIST TO PASS G-REQUEST
page_url_list = [base_url+"?page="+str(x) for x in range(start_page,end_page+1)]

# STARTING FUNCTION
scrape_data(page_url_list)