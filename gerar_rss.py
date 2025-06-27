import requests
from bs4 import BeautifulSoup
from datetime import datetime
from feedgen.feed import FeedGenerator

# URL da página de notícias
URL = "https://www.itupeva.sp.gov.br/noticias"

# Faz requisição
resp = requests.get(URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# Cria o feed
fg = FeedGenerator()
fg.title("Notícias - Prefeitura de Itupeva")
fg.link(href=URL)
fg.description("Últimas notícias de Itupeva")
fg.language("pt-br")

# Pega as notícias
for item in soup.select(".bloco-conteudo .lista-noticias .item"):
    a = item.find("a")
    title = a.get_text(strip=True)
    link = "https://www.itupeva.sp.gov.br" + a["href"]

    date_text = item.select_one(".data").get_text(strip=True)
    pub_date = datetime.strptime(date_text, "%d/%m/%Y")

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=link)
    fe.pubDate(pub_date)

# Salva RSS
fg.rss_file("rss.xml")
print("Feed atualizado com sucesso.")
