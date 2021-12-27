import sqlite3
from bs4 import BeautifulSoup
from requests import get
import time

conn = sqlite3.connect('test.db')
usr_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}





# urls = ['https://www.cleaneatingkitchen.com/', 'https://www.cottercrunch.com/', 'https://downshiftology.com/',
#         'https://fitfoodiefinds.com/', 'https://detoxinista.com/', 'https://www.skinnytaste.com/']





urls = []
with open('urls.txt') as f:
    for line in f:
        url = line.strip()
        if not line.startswith('http'):
            url = 'http://' + line
        urls.append(url)         






tbl_query = '''CREATE TABLE IF NOT EXISTS Item (
Title VARCHAR (255) NOT NULL,
Link VARCHAR(255) NOT NULL,
Content VARCHAR(255));'''
conn.execute(tbl_query)
term = input('Please enter your search term: ')
term = term.strip()

if term == '':
    print('Please enter a search term')
    exit(0)



start = time.time()

for url in urls:
    search_term = f"{term} inurl:{url}"
    escaped_search_term = search_term.replace(' ', '+')
    number_results = 10
    language_code = 'en'

    try:

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results+1,
                                                                            language_code)
        response = get(google_url, headers=usr_agent)    
        response.raise_for_status()
        raw_html = response.text

        results = []
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            content = result.findAll('span')[-1].text
            if link and title and content:
                print(link['href'], title.text, content)
                print()
                
                results.append([title.text, link['href'], content])

        
        conn.executemany("INSERT INTO Item(Title, Link, Content) VALUES (?, ?, ?);", results)
        conn.commit()
    except Exception as e:
        print(e)
    time.sleep(2)

conn.close()

end = time.time()


print('Total Time took in seconds:', (end-start))