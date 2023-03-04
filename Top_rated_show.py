from bs4 import BeautifulSoup
import requests
import pandas as pd

try:
    URL = requests.get('https://www.imdb.com/chart/toptv/?ref_=nv_mp_tv250')
    URL.raise_for_status()
    soup = BeautifulSoup(URL.text, 'lxml')
    
    tv_shows = soup.find('tbody', class_='lister-list').find_all('tr')
    
    data = []
    for tv_show in tv_shows:
        # Extract rank and year
        td = tv_show.find('td', class_='titleColumn')
        rank = td.text.split('.')[0].strip()
        year = td.text.split('(')[-1].split(')')[0].strip()
        
        # Extract title
        title = td.find('a').text
        
        # Extract rating
        rating = tv_show.find('td', class_='ratingColumn imdbRating').text.strip()
        
        data.append([rank, title, year, rating])
    
    # Create DataFrame object and write to Excel file
    df = pd.DataFrame(data, columns=['Rank', 'Title', 'Year', 'Rating'])
    df.to_excel('imdb_top_tv_shows.xlsx', index=False)
    
except Exception as e:
    print(e)
