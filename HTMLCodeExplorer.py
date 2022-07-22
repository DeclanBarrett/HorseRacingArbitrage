from urllib.request import Request, urlopen
from re import findall, finditer, MULTILINE, DOTALL

url = 'https://www.punters.com.au/odds-comparison/horse-racing/all/';
content_file = ""

#Opens the webpage
def open_web_page(page_to_open):
    req = Request(page_to_open, headers={'User-Agent': 'Mozilla/5.0'})
    #Open the target URL
    web_page = urlopen(req)
    try:
        #Extract webpage contents
        web_page_bytes = web_page.read()
        web_page_contents = web_page_bytes.decode('ASCII', 'backslashreplace')
        #Close the page
        web_page.close()
        return web_page_contents
    except OSError:
        return 'Connect to Internet'

content_file = open_web_page(url)
print(content_file)
