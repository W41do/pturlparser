#!/usr/bin/python3
import logging
import requests
from modules.url_extractor import HTMLExtractor, JavaScriptExtractor
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from argparse import ArgumentParser
from sys import path, exit, argv

# import custom libraries - used because of pypi
if __name__ != "__main__":
    path.append(__file__.rsplit("/", 1)[0])

# own libs
from _version import __version__
from ptlibs import ptprinthelper

class pturlparser:

    # Parser object constructor
    def __init__(self, args):
        logging.disable(logging.CRITICAL)
        self.use_json = args.output == "json"
        self.url = args.url
        self.output_format = args.output

    # Parsing execution
    def run(self):
        urls = self.parse_target(self.url)
        self.display_urls(urls)

    # Method to fetch HTML and JS content from target URL and extract URLs from it
    def parse_target(self, target):
        try:
            response = requests.get(target)
            html_content = response.text

        # In case invalid url is inputted
        except requests.RequestException as e:
            print(f"Error loading page {target}: {e}")
            return set()

        # URL extractor initialization
        html_extractor = HTMLExtractor(base_url=target)
        html_urls = html_extractor.extract(html_content)

        # JS extractor initialization
        js_extractor = JavaScriptExtractor()
        # HTML parser initialization
        soup = BeautifulSoup(html_content, 'html.parser')

        # Looks in the children of page elements to find <script> tags
        for script in soup.find_all('script'):
            script_url = script.get('src')
            # If found a URL in src attribute of a <script> tag
            if script_url:
                # Join base URL and relative URL
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

    # shows gathered URLs in JSON or TXT format
    def display_urls(self, urls):
        # Display in console
        if self.output_format == "console":
            for url in urls:
                print(url)
        # Export to JSON
        elif self.output_format == "json":
            with open("output.json", "w") as json_file:
                json.dump(list(urls), json_file, indent=4)
        # Export to TXT
        elif self.output_format == "text":
            with open("output.txt", "w") as file:
                for url in urls:
                    file.write(url + "\n")

    # I'm trying
    # Shows help text
def get_help():
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

# Command line arguments parsing
def parse_args():
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

    use_json = args.output == "json"
    ptprinthelper.print_banner(SCRIPTNAME, __version__, use_json)
    # ptprinthelper.print_banner(SCRIPTNAME, __version__)
    return args

# Main function, parsing command line arguments, parser instance creation.
def main():
    global SCRIPTNAME
    SCRIPTNAME = "pturlparser"
    args = parse_args()
    script = pturlparser(args)
    script.run()


if __name__ == "__main__":
    main()
