from flask import Flask, request, render_template_string
import os, shutil

# --- Configuration ---
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
BACKUP_FOLDER = './backups'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# --- Exemple de fonction de traitement ---
def process_task(file_path, task):
    """
    Refonte ultra design html css en conservant les couleurs de la page.
    Ici tu peux mettre ta logique de refonte HTML/design.
    Pour l'exemple, on lit le fichier, on ajoute un commentaire et on renvoie le contenu.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Exemple simple : ajout d'un commentaire en début
    new_content = f"<!-- Fichier traité pour : {task} -->\n" + content

    # Sauvegarde du fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return new_content

# --- Route principale ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task', 'Refonte et optimisation')
        uploaded_file = request.files.get('file')

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Sauvegarde du fichier uploadé
            uploaded_file.save(file_path)

            # Backup
            shutil.copy(file_path, os.path.join(BACKUP_FOLDER, filename))

            # Traitement (refonte/optimisation)
            result_html = process_task(file_path, task)

            # Affiche le résultat directement dans le navigateur
            return render_template_string(result_html)

        else:
            return "Erreur : aucun fichier reçu.", 400

    # Formulaire HTML moderne
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent IA Développeur</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; background:#f7f9fc; color:#333; }
            .container { max-width: 500px; margin: 5% auto; padding: 30px; background: #fff; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
            h1 { text-align:center; color:#33ACFF; }
            input[type=text], input[type=file], input[type=password] {
                width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #33ACFF; border-radius: 6px; font-size: 16px;
            }
            input[type=text]:hover, input[type=password]:hover { box-shadow: 0 3px 6px rgba(51,172,255,0.3); }
            button { width: 100%; padding: 12px; background:#33ACFF; color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer; }
            button:hover { background:white; color:#33ACFF; border:1px solid #33ACFF; }
            label { font-weight:bold; color:#33ACFF; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>GRH+</h1>
            <form method="POST" enctype="multipart/form-data">
                <label>Fichier HTML :</label>
                <input type="file" name="file" required>
                <label>Tâche :</label>
                <input type="text" name="task" placeholder="Refonte et optimisation" required>
                <button type="submit">Valider</button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

