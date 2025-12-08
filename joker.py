import requests
import re
import sys

# URL till API:et (vi ber om formatet text/plain för enkelhetens skull)
URL = "https://icanhazdadjoke.com/"
HEADERS = {"Accept": "text/plain"}

def get_joke():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status() # Kollar om vi fick felkod (t.ex. 404)
        return response.text
    except Exception as e:
        print(f"Kunde inte hämta skämt: {e}")
        sys.exit(1) # Avsluta med felkod så Action-loggen visar rött

def update_readme(joke):
    readme_path = "README.md"
    
    # Markörer som vi letar efter i filen
    start_marker = "<!-- START -->"
    end_marker = "<!-- END -->"
    
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Skapa ett Regex-mönster för att hitta texten mellan markörerna
    # re.DOTALL gör att . (punkt) även matchar nya rader
    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n\n**Dagens skämt:**\n> {joke}\n\n{end_marker}"
    
    # Byt ut innehållet
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        print("Inga markörer hittades i README.md. Inget uppdaterades.")
    else:
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        print("README.md har uppdaterats med ett nytt skämt!")

if __name__ == "__main__":
    joke = get_joke()
    print(f"Hämtat skämt: {joke}")
    update_readme(joke)
