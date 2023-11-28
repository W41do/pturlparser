from bs4 import BeautifulSoup
import re
import esprima
from urllib.parse import urljoin

class HTMLExtractor:
    """
    Extractor for collecting URLs from HTML content.

    Attributes:
        base_url (str): The base URL to resolve relative URLs against.
        urls (set): A set that keeps track of the extracted URLs.
    """
    def __init__(self, base_url=None):
        self.base_url = base_url  # Target URL
        self.urls = set()  # Set of extracted URLs

    def add_url(self, url):
        """
        Resolves a given URL against the base URL and adds it to the set of URLs.
    
        Args:
            url (str): The URL to be added, either absolute or relative.
        """
        # Ignore mailto links
        if url.startswith('mailto:'):
            return
        try:
            # Joining base URL with relative URL
            normalized_url = urljoin(self.base_url, url) if self.base_url else url
            # Only add http or https URLs
            if normalized_url.startswith(('http://', 'https://')):
                self.urls.add(normalized_url)
        except Exception as e:
            print(f"Error normalizing URL {url}: {e}")

    def extract(self, html_content):
        """
        Extracts URLs from the provided HTML content.

        Args:
            html_content (str): The HTML content to extract URLs from.

        Returns:
            set: The set of extracted URLs.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Dictionary mapping tags to attributes which contain URLs.
        tag_attributes = {
            'a': 'href',
            'link': 'href',
            'script': 'src',
            'img': 'src',
            'iframe': 'src'
        }

        # Nested for loop to extract links from all tags in all elements
        for tag, attribute in tag_attributes.items():
            for element in soup.find_all(tag, attrs={attribute: True}):
                self.add_url(element[attribute])

        # Extracting additional URLs from inline elements.
        self._extract_inline(soup)
        return self.urls

    def _extract_inline(self, soup):
        """
        Extracts URLs from inline elements such as script and style tags.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML.
        """
        # Extracting from <script> tags
        for script in soup.find_all('script'):
            if script.string:
                # Find anything that resembles a https:// url and add it into a list
                urls = re.findall(r'https?://\S+', script.string)
                for url in urls:
                    self.add_url(url)

        # Extracting from <style> tags
        for style in soup.find_all('style'):
            if style.string:
                 # Find anything that resembles a CSS url and add it into a list
                urls = re.findall(r'url\(["\']?(.*?)["\']?\)', style.string)
                for url in urls:
                    self.add_url(url)


class JavaScriptExtractor:
    """
    Extractor for collecting URLs from JavaScript content.

    Attributes:
        urls (set): A set that keeps track of the extracted URLs.
    """
    def __init__(self):
        self.urls = set()

    def _extract_from_node(self, node):
        """
        Recursively extracts URLs found within the syntax nodes of the JavaScript AST (Abstract Syntax Tree).
        """
        if isinstance(node, esprima.nodes.Literal) and isinstance(node.value, str):
            if node.value.startswith(('http://', 'https://')):
                self.urls.add(node.value)
        elif isinstance(node, esprima.nodes.Node) or isinstance(node, list):
            # Check if 'children' method exists and is callable
            if hasattr(node, 'children') and callable(node.children):
                for child in node.children():
                    self._extract_from_node(child)
        elif isinstance(node, list):
            for element in node:
                self._extract_from_node(element)

    def extract(self, js_content):
        """
        Parses JavaScript content and extracts URLs.

        Args:
            js_content (str): The JavaScript code to extract URLs from.

        Returns:
            set: The set of extracted URLs.
        """
        try:
            ast = esprima.parseScript(js_content, tolerant=True, jsx=True)
            self._extract_from_node(ast)
        except Exception as e:
            print(f"Error parsing JavaScript content: {e}")
        return self.urls