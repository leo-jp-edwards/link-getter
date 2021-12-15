import requests
from bs4 import BeautifulSoup

from app.models.tortoise import SubLinkList


async def generate_link_list(list_id: int, url: str) -> None:
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    await SubLinkList.filter(id=list_id).update(sublinks=links)