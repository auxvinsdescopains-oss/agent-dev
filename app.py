from flask import Flask, request, render_template_string, jsonify
from openai import OpenAI
import os, shutil
import time

# --- Flask Config ---
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
BACKUP_FOLDER = './backups'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# --- OpenAI Client ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------
#  IA – AUTOMATIC MODEL FALLBACK (ANTI-429 + ANTI-QUOTA)
# ---------------------------------------------------------
def safe_openai_call(prompt):
    """
    Appel IA avec fallback automatique :
    1️⃣ gpt-4.1 (premium)
    2️⃣ gpt-4o (si dispo)
    3️⃣ gpt-4o-mini (jamais limité)
    """

    MODELS = ["gpt-4.1", "gpt-4o", "gpt-4o-mini"]

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                timeout=40
            )
            print(f"✔ Réussi avec modèle : {model}")
            return response.choices[0].message["content"]

        except Exception as e:
            error = str(e)
            print(f"⚠ Erreur avec {model}: {error}")

            # Cas quota ou limitation → on passe au modèle suivant
            if ("quota" in error.lower() or
                "limit" in error.lower() or
                "429" in error.lower()):
                continue  # On tente le modèle suivant

            # Autres erreurs → stop
            raise e

    return "Erreur : aucun modèle OpenAI n'est disponible."


# ---------------------------------------------------------
#  IA – Refonte HTML/CSS future Design
# ---------------------------------------------------------
def ai_restyle_html(content, task):
    prompt = f"""
    Tu es un expert UI/UX, spécialisé en web design futuriste.
    Refonte complète du code HTML/CSS suivant.

    Objectifs :
    - style ultra moderne
    - animations fluides
    - glassmorphism / neomorphism
    - responsive mobile
    - transitions premium
    - code propre
    - conserver les couleurs existantes
    - garder les textes

    Tâche demandée : {task}

    Retourne uniquement le code final.

    CODE :
    {content}
    """
    return safe_openai_call(prompt)


# ---------------------------------------------------------
#  Traitement fichier uploadé
# ---------------------------------------------------------
def process_task(file_path, task):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = ai_restyle_html(content, task)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return new_content


# ---------------------------------------------------------
#  Page FORMULAIRE
# ---------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task', 'Refonte moderne')
        uploaded_file = request.files.get('file')

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            uploaded_file.save(file_path)
            shutil.copy(file_path, os.path.join(BACKUP_FOLDER, filename))

            result_html = process_task(file_path, task)
            return render_template_string(result_html)

        return "Erreur : aucun fichier reçu.", 400

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent IA Développeur</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; background:#eef3fa; color:#333; }
            .container {
                max-width: 520px; margin: 5% auto; padding: 30px; background:#fff;
                border-radius: 14px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            h1 { text-align:center; color:#33ACFF; }
            input[type=text], input[type=file] {
                width: 100%; padding: 12px; margin: 10px 0;
                border: 1px solid #33ACFF; border-radius: 6px; font-size: 16px;
            }
            button {
                width: 100%; padding: 12px; background:#33ACFF; color:white;
                border:none; border-radius:6px; font-size:16px; cursor:pointer;
            }
            button:hover {
                background:white; color:#33ACFF; border:1px solid #33ACFF;
            }
            label { font-weight:bold; color:#33ACFF; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GRH+ Designer IA</h1>
            <form method="POST" enctype="multipart/form-data">
                <label>Fichier HTML :</label>
                <input type="file" name="file" required>
                <label>Tâche :</label>
                <input type="text" name="task" placeholder="Refonte ultra design" required>
                <button type="submit">Valider</button>
            </form>
        </div>
    </body>
    </html>
    '''


# ---------------------------------------------------------
#  API REST : restyle code brut via JSON
# ---------------------------------------------------------
@app.route('/restyle', methods=['POST'])
def restyle():
    code = request.json.get("code", "")
    task = request.json.get("task", "Refonte moderne API")

    result = ai_restyle_html(code, task)
    return jsonify({"restyled": result})


# ---------------------------------------------------------
#  Local run (Render n’utilise pas ce bloc)
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
