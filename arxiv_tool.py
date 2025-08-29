#Access arxiv using url
import requests
import xml.etree.ElementTree as ET

def search_arxiv_paper(topic: str,max_results: int=5) -> dict:
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            print(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")
        
    url = (
            "http://export.arxiv.org/api/query"
            f"?search_query=all:{query}"
            f"&max_results={max_results}"
            "&sortBy=submittedDate"
            "&sortOrder=descending"
        )
    resp = requests.get(url)
    if not resp.ok:
        print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
        raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")
    
    data = parse_arxiv_xml(resp.text)
    return data


#parsing xml
def parse_arxiv_xml(xml_content: str) -> dict:
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)
    for entry in root.findall("atom:entry",ns):
        authors = [
            author.findtext("atom:name",namespace=ns)
            for author in entry.findall("atom:author",ns)
        ]

        categories = [
            cat.attrib.get("term")
            for cat in entry.finall("atom:category",ns)
        ]

        pdf_link = None
        for link in entry.findall("atom:link",ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break
        entries.append({
            "title": entry.findtext("atom:title",namespaces=ns),
            "summary":entry.findtext("atom:summary",namespaces=ns).strip(),
            "authors":authors,
            "categories": categories,
            "pdf": pdf_link
        })
    return {"entries": entries}

