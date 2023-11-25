from bs4 import BeautifulSoup
import esprima
import re
from urllib.parse import urljoin

class HTMLExtractor:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.urls = set()

    def add_url(self, url):
        try:
            normalized_url = urljoin(self.base_url, url) if self.base_url else url
            self.urls.add(normalized_url)
        except Exception as e:
            print(f"Error normalizing URL {url}: {e}")

    def extract(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        tag_attributes = {'a': 'href', 'link': 'href', 'script': 'src', 'img': 'src', 'iframe': 'src'}
        
        for tag, attribute in tag_attributes.items():
            for element in soup.find_all(tag, attrs={attribute: True}):
                self.add_url(element[attribute])

        self._extract_inline(soup)
        return self.urls

    def _extract_inline(self, soup):
        for script in soup.find_all('script'):
            if script.string:
                potential_urls = re.findall(r'https?://\S+', script.string)
                for url in potential_urls:
                    self.add_url(url)

        for style in soup.find_all('style'):
            if style.string:
                potential_urls = re.findall(r'url\(["\']?(.*?)["\']?\)', style.string)
                for url in potential_urls:
                    self.add_url(url)


class JavaScriptExtractor:
    def __init__(self):
        self.urls = set()

    def extract_from_node(self, node):
        if isinstance(node, esprima.nodes.Literal) and isinstance(node.value, str):
            if 'http://' in node.value or 'https://' in node.value:
                self.urls.add(node.value)
        elif isinstance(node, esprima.nodes.Node):
            for child in node:
                self.extract_from_node(child)
        elif isinstance(node, list):
            for element in node:
                self.extract_from_node(element)

    def extract(self, js_content):
        try:
            ast = esprima.parseScript(js_content, tolerant=True, jsx=True)
            self.extract_from_node(ast)
        except Exception as e:
            print(f"Error parsing JavaScript content: {e}")
        return self.urls