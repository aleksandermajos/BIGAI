import requests
from bs4 import BeautifulSoup
req = requests.get("https://context.reverso.net/translation/spanish-english/tímido", headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(req.text, 'html.parser')
sentences = [x.text.strip() for x in soup.find_all('span', {'class':'text'}) if '\n' in x.text]
type(sentences)