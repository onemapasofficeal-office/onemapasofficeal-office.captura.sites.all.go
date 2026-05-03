import requests
from bs4 import BeautifulSoup
import base64
import time
import os
import random
from urllib.parse import urljoin, urlparse

# --- CONFIGURAÇÕES ---
TOKEN = "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" 
REPO = "onemapasofficeal-office/onemapasofficeal-office.github.io"
PASTA_TEMP = "temp_capture"

for p in [PASTA_TEMP, f"{PASTA_TEMP}/img"]:
    if not os.path.exists(p): os.makedirs(p)

def upload_github(caminho_local, nome_github):
    url = f"https://api.github.com/repos/{REPO}/contents/{nome_github}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    try:
        with open(caminho_local, "rb") as f:
            conteudo = f.read()

        res_get = requests.get(url, headers=headers)
        sha = res_get.json().get("sha") if res_get.status_code == 200 else None
        
        dados = {
            "message": f"🤖 Upload: {nome_github}",
            "content": base64.b64encode(conteudo).decode("utf-8")
        }
        if sha: dados["sha"] = sha
        
        res = requests.put(url, json=dados, headers=headers)
        return res.status_code in [200, 201]
    except:
        return False

def atualizar_index(novos_arquivos):
    url_index = f"https://api.github.com/repos/{REPO}/contents/index.html"
    headers = {"Authorization": f"token {TOKEN}"}
    res = requests.get(url_index, headers=headers)
    
    conteudo_base = "<html><body><h1>Links</h1><div id='links'></div></body></html>"
    sha = None
    if res.status_code == 200:
        conteudo_base = base64.b64decode(res.json()['content']).decode('utf-8')
        sha = res.json()['sha']

    novos_links = "".join([f"<p>🖼️ <a href='{a}'>{a}</a></p>\n" for a in novos_arquivos])
    novo_html = conteudo_base.replace("<div id='links'>", f"<div id='links'>\n{novos_links}")
    
    requests.put(url_index, json={
        "message": "Update Index",
        "content": base64.b64encode(novo_html.encode('utf-8')).decode('utf-8'),
        "sha": sha
    }, headers=headers)

def iniciar():
    print("--- 🚀 MODO MULTIMÍDIA INFINITO ---")
    url_inicial = input("🔗 URL Inicial: ").strip()
    fila = [url_inicial]
    visitados = set()
    
    while True:
        lote_arquivos = []
        print(f"\n📡 Coletando novo lote de 50 sites e suas imagens...")

        while len(lote_arquivos) < 50 and fila:
            url = fila.pop(0)
            if url in visitados: continue
            
            try:
                res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if res.status_code == 200:
                    prefixo = urlparse(url).netloc.replace(".","_") + str(random.randint(100,999))
                    nome_html = f"{prefixo}.html"
                    caminho_html = os.path.join(PASTA_TEMP, nome_html)
                    
                    soup = BeautifulSoup(res.text, "html.parser")
                    
                    # --- BAIXAR IMAGENS DO SITE ---
                    for img in soup.find_all("img", src=True):
                        img_url = urljoin(url, img["src"])
                        img_nome = f"img/{prefixo}_" + os.path.basename(urlparse(img_url).path)
                        if not img_nome.endswith(('.jpg', '.png', '.gif', '.webp')): img_nome += ".jpg"
                        
                        try:
                            img_res = requests.get(img_url, timeout=3)
                            if img_res.status_code == 200:
                                with open(os.path.join(PASTA_TEMP, img_nome), "wb") as f:
                                    f.write(img_res.content)
                                lote_arquivos.append({"local": os.path.join(PASTA_TEMP, img_nome), "github": img_nome})
                                img["src"] = img_nome # Atualiza o HTML para usar a imagem local
                        except: continue

                    with open(caminho_html, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    
                    lote_arquivos.append({"local": caminho_html, "github": nome_html})
                    visitados.add(url)
                    
                    for a in soup.find_all("a", href=True):
                        fila.append(urljoin(url, a["href"]))
            except: continue

        print(f"📤 Subindo {len(lote_arquivos)} arquivos (HTMLs + Imagens)...")
        htmls_enviados = []
        for item in lote_arquivos:
            if upload_github(item["local"], item["github"]):
                if item["github"].endswith(".html"): htmls_enviados.append(item["github"])
            if os.path.exists(item["local"]): os.remove(item["local"])

        atualizar_index(htmls_enviados)
        print("⏳ Aguardando 30s para o próximo ciclo (enquanto o GitHub processa)...")
        time.sleep(30)

if __name__ == "__main__":
    iniciar()
