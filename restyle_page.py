import requests

# URL de ton agent Render
url = "https://agent-dev-1.onrender.com/task"

# Page HTML à restyler (copie de test)
file_path = "test_pages/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

payload = {
    "task": "Refonds cette page HTML avec un design moderne, responsive et élégant. Ne rien toucher en ligne.",
    "html": html_content
}

response = requests.post(url, json=payload)

optimized_html = response.text

# Sauvegarde du résultat dans un nouveau fichier
output_file = "test_pages/index_optimized.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(optimized_html)

print(f"Page restylée ! Ouvre {output_file} pour voir le résultat.")
