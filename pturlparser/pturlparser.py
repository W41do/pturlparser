#!/usr/bin/env python3
import logging
import requests
from modules.url_extractor import HTMLExtractor, JavaScriptExtractor
import json
from argparse import ArgumentParser
from sys import argv, exit, path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Import custom libraries - used for PyPI installations.
if __name__ != "__main__":
    path.append(__file__.rsplit("/", 1)[0])

# Own libraries
from _version import __version__
from ptlibs import ptprinthelper

logging.disable(logging.CRITICAL)

SCRIPTNAME = "pturlparser"

class PTUrlParser:
    """ 
    A class used to parse and extract URLs from an HTML page and its JavaScript sources.
    
    Attributes:
        url: The target URL to analyze.
        output_format: The format in which to output the extracted URLs.
    """
    def __init__(self, args):
        self.url = args.url
        self.output_format = args.output

    def run(self):
        """ Main entry point for running the URL parsing logic. """
        urls = self.parse_target(self.url)
        self.display_urls(urls)

    def parse_target(self, target):
        """ Fetches HTML and JS content from the target URL and extracts URLs. """
        try:
            response = requests.get(target)
            html_content = response.text
        except requests.RequestException as e:
            print(f"Error loading page {target}: {e}")
            return set()

        # URL extractor initialization
        html_extractor = HTMLExtractor(base_url=target)
        html_urls = html_extractor.extract(html_content)

        # JS extractor initialization
        js_extractor = JavaScriptExtractor()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

         # Looks in the children of page elements to find <script> tags
        for script in soup.find_all('script'):
            script_url = script.get('src')
            # If found a URL in src attribute of a <script> tag
            if script_url:
                # Creating the absolute URL for the script src
                full_script_url = urljoin(target, script_url)
                try:
                     # Get full url list
                    script_response = requests.get(full_script_url)
                    html_urls.update(js_extractor.extract(script_response.text))
                except requests.RequestException as e:
                    print(f"Error loading script {full_script_url}: {e}")
            elif script.string:
                # update URL list
                html_urls.update(js_extractor.extract(script.string))

        return html_urls

    def display_urls(self, urls):
        """ Shows the gathered URLs in the specified format. """
        if self.output_format == "console": # Display in console
            for url in urls:
                print(url)
        else:
            filename = f'output.{self.output_format}'
            with open(filename, "w") as f:
                if self.output_format == "json": # Export to JSON
                    json.dump(list(urls), f, indent=4)
                elif self.output_format == "text": # Export to TXT
                    f.writelines(f'{url}\n' for url in urls)

def get_help(): # I'm trying
    """ Shows information about the functionality and syntax. """
    return [
        {"description": ["pturlparser"]},
        {"description": [
            "Tool for extracting URLs from HTML and JavaScript"]},
        {"usage": ["pturlparser <options>"]},
        {"usage_example": [
            "pturlparser -u https://www.example.com",
        ]},
        {"options": [
            ["-u", "--url", "<url>", "Specify the target URL to analyze"],
            ["-o", "--output", "<format>", "Set the output format (console, json, text)"],
            ["-h", "--help", "", "Show this help message"],
            ["-v", "--version", "", "Display the version of the tool"],
        ]
        }]


def parse_args():
    """ Parsing function that will parse command line arguments. """
    parser = ArgumentParser(
        add_help=False, usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-u", "--url", dest="url", help="Specify the target URL to analyze")
    parser.add_argument("-o", "--output", choices=['console', 'json', 'text'], default='console', 
                        help="Set the output format (console, json, text)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")

    if len(argv) == 1 or "-h" in argv or "--help" in argv:
        ptprinthelper.help_print(get_help(), SCRIPTNAME, __version__)
        exit(0)
    args = parser.parse_args()

    ptprinthelper.print_banner(SCRIPTNAME, __version__)
    return args

def main():
    """ Main function that initializes and runs the URL parser. """    
    # Parse command-line arguments to configure the parser's behavior.
    args = parse_args()
    # Create and execute the URL parsing procedure based on the provided arguments.
    parser_instance = PTUrlParser(args)
    parser_instance.run()

if __name__ == "__main__":
    main()
