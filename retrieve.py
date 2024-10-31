import requests
from bs4 import BeautifulSoup
import pandas as pd

from pprint import pprint

reverse_index = {}

def parse_table(table_url):
    # Send a GET request to the URL
    # response = requests.get(table_url)
    
    # # Check if the request was successful
    # if response.status_code != 200:
    #     print(response.status_code)
    #     return None
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(open(table_url, encoding="utf8"), 'html.parser')

    titles_data = []
    # Find all titles
    titles = soup.find_all('h2')

    for title in titles:
        span = title.find('span')
        if span is not None:
            titles_data.append(span.text)
    titles_data = [t[5:].replace('"', '') for t in titles_data[:-2]]
    titles_data.insert(45, 'Ryu-Kishin Powered')
    titles_data.insert(55, 'Bracchio-raidus')


    # Find all tables on the page
    tables = soup.find_all('tbody')
    
    # Initialize an empty list to store the extracted data
    data = []
 
    # Iterate over each table and extract the rows and columns
    for title, table in zip(titles_data, tables[1:]):
        # Get the rows of the table
        rows = table.find_all('tr')
        
        # Create a pandas DataFrame from the table data
        
        for row in rows:
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell)
                # if isinstance(cell, str) and '<' in cell:
                #     # Assuming the cell is a header or title, skip it
                #     continue
                # elif isinstance(cell, pd.Series):
                #     row_data.append(cell.values.tolist())
                # else:
                #     row_data.append(str(cell))
            
            if len(row_data) > 0:
                for m in row_data[0].find('ul').find_all('li'):
                    material = m.find('a')
                    if material.text not in reverse_index:
                        reverse_index[material.text] = {}
                    if title not in reverse_index[material.text]:
                        reverse_index[material.text][title] = []
                        reverse_index[material.text][title].append((row_data[1], 1))
                        reverse_index[material.text]['card_url'] = material
                for m in row_data[1].find('ul').find_all('li'):
                    material = m.find('a')
                    if material.text not in reverse_index:
                        reverse_index[material.text] = {}
                    if title not in reverse_index[material.text]:
                        reverse_index[material.text][title] = []
                        reverse_index[material.text][title].append((row_data[0], 2))
                        reverse_index[material.text]['card_url'] = material
        data.append(row_data)
        
    
    # Return the extracted data
    return data

def main():
    url = 'C:/Users/darth/Code/yu-gi-oh-dor-fusions-reverse-index/yugipedia.htm'
    tables = parse_table(url)
    duplicates = set()
    with open('reverse_index.htm', 'w') as w:
        w.write("<html><body>")
        w.write('<a href="https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_The_Duelists_of_the_Roses_Fusions">Original fusion list:</a>')
        w.write('<hr/>')
        for k in reverse_index:
            w.write(f'<h1>#{reverse_index[k]['card_url']}</h1>')
            for t, v in reverse_index[k].items():
                if t != 'card_url':
                    w.write(f'<h3>{t}</h3>')
                    for material in v:
                        w.write(f'<h4>When used in position {(material[1])}:</h4>')
                        w.write(str(material[0]))
                        w.write('<hr/>')

        w.write("<body></html>")

if __name__ == "__main__":
    main()