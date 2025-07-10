import json
import pathlib
import requests

from bs4 import BeautifulSoup

BASE_URL = "https://ocw.mit.edu"


def main():
    input_path = pathlib.Path("keats-search-eval/data/slides/urls/courses.json")
    output_path = pathlib.Path("keats-search-eval/data/slides/urls/urls.json")

    with open(input_path) as f:
        metadata = json.load(f)

    data = {}

    for module_id, entry in metadata.items():
        course_url = entry["url"]
        if not course_url:
            raise ValueError(f"Skipping course {module_id}: no URL found")

        # Get the list of lecture resource pages
        response = requests.get(course_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Step Find all links to individual lecture resource pages
        resource_links = [
            BASE_URL + a["href"]
            for a in soup.find_all("a", href=True)
            if "/resources/" in a["href"]
        ]

        # Visit each lecture resource page and extract PDF URL
        pdf_urls = []

        for link in resource_links:
            res_page = requests.get(link)
            res_soup = BeautifulSoup(res_page.text, "html.parser")

            # Look for the PDF link (usually in an <a> tag with .pdf in href)
            pdf_link = res_soup.find("a", href=lambda x: x and x.endswith(".pdf"))
            if pdf_link:
                full_pdf_url = BASE_URL + pdf_link["href"]
                pdf_urls.append(full_pdf_url)
                print(f"Found: {full_pdf_url}")

        data[module_id] = pdf_urls
        print(f"Found {len(pdf_urls)} pdfs for module {module_id}")

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved PDF URLs to: {output_path}")


if __name__ == "__main__":
    main()
