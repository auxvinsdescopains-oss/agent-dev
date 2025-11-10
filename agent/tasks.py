# Pour l'instant, ce module peut évoluer pour gérer une queue de tâches
tasks = []

def add_task(file_path, task_desc):
    tasks.append({'file': file_path, 'task': task_desc})
