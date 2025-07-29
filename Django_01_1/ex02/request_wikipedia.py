import requests
import dewiki
import re

def request_wikipedia(keyword: str) -> dict:
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
        "titles": keyword
        # On retire "exintro": True
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    if "missing" not in page:
        return page

    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": keyword
    }
    search_response = requests.get(url, params=search_params)
    search_data = search_response.json()
    search_results = search_data["query"]["search"]
    if search_results:
        best_title = search_results[0]["title"]
        params["titles"] = best_title
        response = requests.get(url, params=params)
        page = next(iter(response.json()["query"]["pages"].values()))
        return page
    else:
        return {"error": "No result."}

def get_image_url(title: str) -> str:
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "original",
        "titles": title
    }
    response = requests.get(url, params=params)
    data = response.json()
    pages = data["query"]["pages"]
    for page in pages.values():
        if "original" in page:
            return page["original"]["source"]
    return ""

def create_file(result_wiki: dict):
    title = result_wiki.get("title", "result")
    extract = result_wiki.get("extract", "")
    if not extract:
        print("Aucun contenu à enregistrer.")
        return
    clean_text = dewiki.from_string(extract)
    filename = re.sub(r'[\\/*?:"<>|]', "_", title) + ".wiki"
    image_url = get_image_url(title)
    wiki_url = f"https://fr.wikipedia.org/wiki/{title.replace(' ', '_')}"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"=== {title.center(40)} ===\n\n")
        if image_url:
            file.write(f"[Image] : {image_url}\n\n")
        file.write(f"{clean_text}\n\n")
        file.write(f"Source : {wiki_url}\n")
    print(f"Fichier créé : {filename}")


if __name__ == "__main__":
    keyword = input("Enter the search : ")
    result = request_wikipedia(keyword)
    if "error" in result:
        print("No result")
    else:
        create_file(result)