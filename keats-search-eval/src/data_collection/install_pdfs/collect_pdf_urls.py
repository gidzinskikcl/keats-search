import requests
from bs4 import BeautifulSoup
import os

# Step 1: URL to the lecture materials page
base_url = "https://ocw.mit.edu"
main_url = "https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/pages/lecture-slides-and-files/"

# Step 2: Get the list of lecture resource pages
response = requests.get(main_url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Find all links to individual lecture resource pages
resource_links = [
    base_url + a["href"]
    for a in soup.find_all("a", href=True)
    if "/resources/" in a["href"]
]

# Step 4: Visit each lecture resource page and extract PDF URL
pdf_urls = []

for link in resource_links:
    res_page = requests.get(link)
    res_soup = BeautifulSoup(res_page.text, "html.parser")

    # Look for the PDF link (usually in an <a> tag with .pdf in href)
    pdf_link = res_soup.find("a", href=lambda x: x and x.endswith(".pdf"))
    if pdf_link:
        full_pdf_url = base_url + pdf_link["href"]
        pdf_urls.append(full_pdf_url)
        print(f"Found: {full_pdf_url}")

# Optional: Download the PDFs
os.makedirs("mit_pdfs", exist_ok=True)

for url in pdf_urls:
    filename = os.path.join("mit_pdfs", url.split("/")[-1])
    print(f"Downloading {filename}...")
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
