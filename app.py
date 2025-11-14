from flask import Flask, request, render_template_string, jsonify
from openai import OpenAI
import os, shutil

# --- Configuration ---
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
BACKUP_FOLDER = './backups'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# --- OpenAI ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- IA : fonction de restyle HTML ---
def ai_restyle_html(content, task):
    prompt = f"""
    Tu es un expert UI/UX, spécialisé en web design futuriste.
    Refonte complète du code HTML/CSS suivant.
    
    Objectifs :
    - design ultra moderne
    - animations élégantes
    - glassmorphism
    - responsive
    - effets premium
    - composants stylés
    - respecter les couleurs existantes
    - garder le contenu textuel
    - améliorer la structure si nécessaire

    Tâche demandée : {task}

    Retourne uniquement le code final (HTML/CSS/JS), sans commentaires supplémentaires.

    CODE A RESTYLER :
    {content}
    """

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]


# --- TRAITEMENT FICHIER UPLOADE ---
def process_task(file_path, task):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Appel à l'IA
    new_content = ai_restyle_html(content, task)

    # Sauvegarde du fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return new_content


# ------------------------------
# PAGE PRINCIPALE (FORMULAIRE)
# ------------------------------
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

            # On affiche le résultat en pleine page
            return render_template_string(result_html)

        return "Erreur : aucun fichier reçu.", 400

    # Formulaire HTML modernisé
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent IA Développeur</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; background:#f1f5fb; color:#333; }
            .container {
                max-width: 520px; margin: 5% auto; padding: 30px; background: #fff;
                border-radius: 14px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            h1 { text-align:center; color:#33ACFF; margin-bottom:20px; }
            input[type=text], input[type=file] {
                width: 100%; padding: 12px; margin: 10px 0;
                border: 1px solid #33ACFF; border-radius: 6px; font-size: 16px;
            }
            button {
                width: 100%; padding: 12px; background:#33ACFF; color:white;
                border:none; border-radius:6px; font-size:16px; cursor:pointer;
            }
            button:hover { background:white; color:#33ACFF; border:1px solid #33ACFF; }
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


# ------------------------------
# API RESTYLE JSON (code brut)
# ------------------------------
@app.route('/restyle', methods=['POST'])
def restyle():
    code = request.json.get("code", "")

    result = ai_restyle_html(code, "Refonte UI moderne API")
    return jsonify({"restyled": result})


# ------------------------------
# RUN (Render ignore ce bloc, mais ok en local)
# ------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
