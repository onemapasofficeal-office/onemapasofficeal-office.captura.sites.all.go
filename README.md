# 🚀 captura-go

Este aplicativo "captura" páginas HTML completas de qualquer lugar da internet e as organiza em um portal automático no GitHub Pages.

## 📖 Como baixar e configurar

Para rodar este script, é necessário ter o **Python** instalado no seu computador.

### 1. Instale o Python
Baixe a versão mais recente diretamente do site oficial:
* [Download Python](https://www.python.org/downloads/)
* [Versão sugerida (3.13+)](https://www.python.org/downloads/release/python-3130/)

### 2. Instale as Bibliotecas Necessárias
Após instalar o Python, abra o seu **CMD** (Prompt de Comando) e execute o comando abaixo:
```bash
pip install requests beautifulsoup4
```
# 🚀 Como Usar
Abra o CMD na pasta onde você baixou o arquivo.

Inicie o script com o comando:

```Bash
python captura-go.py
```
URL Inicial: O app perguntará por onde começar.

Exemplo: https://google.com

Quantidade de Páginas: Defina o limite de capturas.

Exemplo: Se você digitar um número alto como 999999, o robô continuará capturando links sem parar.

Exemplo de Logs no Terminal:
```bash
C:\Users\Downloads>python captura-go.py
Digite a URL inicial: [https://google.com](https://google.com)
Quantas páginas quer baixar no total? 500
🚀 Capturando: [https://google.com](https://google.com)
✅ Enviado: google_com.html
🚀 Capturando: [https://mail.google.com/mail/&ogbl](https://mail.google.com/mail/&ogbl)
```
# 🌐 Visualize os Resultados
Todo o conteúdo capturado é enviado para o repositório e pode ser visualizado online:

🔗 [sites capturados](https://onemapasofficeal-office.github.io)

Desenvolvido por OneMapas Office 

