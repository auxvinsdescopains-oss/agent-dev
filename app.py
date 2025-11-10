from flask import Flask, request, render_template, send_file
from agent.core import process_task  # ton code agent

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        file = request.files.get("file")
        task = request.form.get("task")
        if file and task:
            content = file.read().decode("utf-8")
            result = process_task(content, task)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
