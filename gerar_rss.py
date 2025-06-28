import requests
from bs4 import BeautifulSoup
from datetime import datetime
from feedgen.feed import FeedGenerator

URL = "https://www.itupeva.sp.gov.br/noticias"

resp = requests.get(URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

fg = FeedGenerator()
fg.title("Notícias - Prefeitura de Itupeva")
fg.link(href=URL)
fg.description("Últimas notícias de Itupeva")
fg.language("pt-br")

# Seleciona todas as <li> dentro de <ul class="list-news">
for item in soup.select("ul.list-news li"):
    a = item.find("a")
    if not a:
        continue
    title = a.get_text(strip=True)
    link = "https://www.itupeva.sp.gov.br" + a["href"]

    date_span = item.find("span", class_="date")
    if date_span:
        date_text = date_span.get_text(strip=True)
        try:
            pub_date = datetime.strptime(date_text, "%d/%m/%Y")
        except ValueError:
            pub_date = datetime.now()
    else:
        pub_date = datetime.now()

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.pubDate(pub_date)

fg.rss_file("rss.xml")
print("Feed atualizado com sucesso.")
