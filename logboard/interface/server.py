import time
import json
import threading

from typing import Dict, List
from flask_socketio import SocketIO, emit
from manager.log_manager import LogManager
from utilities.sample_logs import add_sample_logs
from utilities.system_monitor import get_system_performance
from flask import Flask, jsonify, send_from_directory, request, Response

app = Flask(__name__, static_folder="../public")
socketio = SocketIO(app, cors_allowed_origins="*")
log_manager = LogManager(directory="./logs")

def send_performance_periodically():
    """Envoie les performances du système via WebSocket toutes les 2 secondes."""
    while True:
        performance = get_system_performance()
        socketio.emit("performance", performance)
        time.sleep(2)

@app.route("/performance", methods=["GET"])
def get_performance() -> Response:
    """Récupère les performances actuelles du système.

    Returns:
        Dict[str, float]: Dictionnaire avec l'utilisation du CPU, RAM et GPU (si disponible).
    """
    return jsonify(get_system_performance())

@app.route("/logs", methods=["GET"])
def get_logs() -> Response:
    """Récupère les journaux stockés.

    Returns:
        List[Dict]: Liste des journaux sous forme de dictionnaires.
    """
    level = request.args.get("level")
    logs = log_manager.read_logs(filter_level=level)
    return jsonify([log.to_dict() for log in logs])

@app.route("/logs/clear", methods=["POST"])
def clear_logs() -> Response:
    """Supprime tous les journaux dans le fichier logs.json.

    Returns:
        Dict[str, str]: Message de confirmation.
    """
    with open(log_manager.log_file, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)
    return jsonify({"message": "Journaux supprimés avec succès"})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static(path: str) -> Response:
    """Sert les fichiers statiques depuis le dossier public.

    Args:
        path (str): Chemin du fichier demandé (ex. "index.html").

    Returns:
        str: Fichier statique ou index.html si aucun chemin n'est spécifié.
    """
    if not path or path == "index.html":
        return send_from_directory("../public", "index.html")
    return send_from_directory("../public", path)

@socketio.on("connect")
def handle_connect():
    """Gère la connexion d'un client WebSocket."""
    emit("message", {"data": "Connecté au serveur WebSocket"})

if __name__ == "__main__":
    # Lancer le thread pour envoyer les performances périodiquement
    add_sample_logs()
    threading.Thread(target=send_performance_periodically, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)