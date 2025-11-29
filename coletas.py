import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

# URLs das páginas
URLS = {
    "milho_dourados": "https://www.noticiasagricolas.com.br/cotacoes/milho",
    "sorgo_candidomota": "https://www.noticiasagricolas.com.br/cotacoes/sorgo",
    "farelo_mato_grosso": "https://www.noticiasagricolas.com.br/cotacoes/farelo-de-soja"
}

ALVOS = {
    "milho_dourados": "Dourados",
    "sorgo_candidomota": "Cândido Mota",
    "farelo_mato_grosso": "Mato Grosso"
}

def extrair_preco(html, alvo):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            nome = tds[0].get_text(strip=True)
            preco = tds[1].get_text(strip=True)
            if alvo.lower() in nome.lower():
                return preco
    return None

def salvar(nome, preco):
    os.makedirs("historico", exist_ok=True)
    path = f"historico/{nome}.csv"
    hoje = datetime.now().strftime("%Y-%m-%d")
    linha = f"{hoje},{preco}\n"

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("data,preco\n")
    with open(path, "a") as f:
        f.write(linha)

def main():
    for chave, url in URLS.items():
        print(f"Buscando {chave}...")
        r = requests.get(url, headers=HEADERS)
        preco = extrair_preco(r.text, ALVOS[chave])

        if preco:
            salvar(chave, preco)
            print(f"{chave}: {preco}")
        else:
            print(f"❗ Não encontrado: {chave}")

if __name__ == "__main__":
    main()
