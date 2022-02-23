import requests
from bs4 import BeautifulSoup
import json

main_url = 'https://ru.startup.network/startups/page'
projects_data = []


def get_html(url):
    headers = {
        "user-agent":
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    return res.content


def find_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    url_list = [
        url.get('href')
        for url in soup.find('div', class_="projects_list_c").find_all(
            'a', class_="projects_list_b")
    ]
    return url_list


def make_html(url, project_name, card_counter):
    with open(f'data/{card_counter}_{project_name}.html', 'wb') as f:
        f.write(get_html(url))

def make_json(data):
    with open('data.json', 'w', encoding='utf-8-sig') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    card_counter = 0
    for page_number in range(1, 2):
        
        html = get_html(main_url + f'/{page_number}/')

        url_list = find_urls(html)

        for url in url_list:
            content = get_html(url)
            soup = BeautifulSoup(content, 'lxml')
            card_counter += 1

            try:
                project_name = soup.find('h1', itemprop="name").text
            except:
                project_name = ""

            try:
                project_link = soup.find('div',
                                        class_="v_c_ha").get('data-ytvideo')
            except:
                project_link = ""

            try:
                project_idea = soup.find('span', itemprop="description").text
            except:
                project_idea = ""

            try:
                project_idea = soup.find('span', itemprop="description").text
            except:
                project_idea = ""

            symbols_replace = [', ', ' ', '-', '/']
            symbols_delete = ["'", '"', '|', '*']
            
            for symbol in symbols_delete:
                if symbol in project_name:
                    project_name = project_name.replace(symbol, '')
                
            for symbol in symbols_replace:
                if symbol in project_name:
                    project_name = project_name.replace(symbol, '_')
                    
            if project_name != "":
                data = {
                    'project_name': project_name,
                    'project_link': project_link,
                    'project_idea': project_idea
                }

                projects_data.append(data)
                make_html(url, project_name, card_counter)
            else:
                card_counter -= 1
        
    make_json(projects_data)

if __name__ == '__main__':
    main()