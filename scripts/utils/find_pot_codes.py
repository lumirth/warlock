import requests
from bs4 import BeautifulSoup

# NOTE: This script will NECESSARILY be less reliable because it scrapes the
# HTML of the search form. If the search form changes, this script will break.

URL = "https://courses.illinois.edu/search/form"


def fetch_html(url):
    response = requests.get(url)
    return response.text


def parse_html(html_content):
    return BeautifulSoup(html_content, "html.parser")


def extract_part_of_term_options(parsed_html):
    select_element = parsed_html.find("select", {"id": "partOfTerm"})
    option_elements = select_element.find_all("option")
    return option_elements


def create_part_of_term_dict(option_elements):
    part_of_term_dict = {
        option.text.strip(): option.get("value")
        for option in option_elements
        if option.text.strip()  # Ignore empty option names
    }
    return part_of_term_dict


def retrieve_part_of_terms():
    html_content = fetch_html(URL)
    parsed_html = parse_html(html_content)
    option_elements = extract_part_of_term_options(parsed_html)
    return create_part_of_term_dict(option_elements)


if __name__ == "__main__":
    print(retrieve_part_of_terms())
