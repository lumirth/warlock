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


def extract_college_code_options(parsed_html):
    select_element = parsed_html.find("select", {"id": "collegeCode"})
    option_elements = select_element.find_all("option")
    return option_elements


def create_college_code_dict(option_elements):
    college_code_dict = {
        option.text.strip(): option.get("value")
        for option in option_elements
        if option.text.strip()  # Ignore empty option names
    }
    return college_code_dict

def retrieve_college_codes():
    html_content = fetch_html(URL)
    parsed_html = parse_html(html_content)
    option_elements = extract_college_code_options(parsed_html)
    return create_college_code_dict(option_elements)

if __name__ == "__main__":
    retrieve_college_codes()
