from pathlib import Path
from config import AIProjectConfig, convert_paths
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='public', static_url_path='/')

# Chemin vers le fichier JSON de configuration
CONFIG_PATH = Path("config.json")

# Charger la configuration au démarrage
config = AIProjectConfig.from_json(CONFIG_PATH)

@app.route('/config', methods=['GET'])
def get_config():
    """
    Retourner la configuration complète au format JSON.
    """
    return jsonify(config_as_dict()), 200


@app.route('/config', methods=['POST'])
def update_config():
    """
    Mettre à jour la configuration avec les données envoyées (JSON).
    Remplace toute la configuration actuelle.
    """
    global config
    try:
        data = request.get_json(force=True)
        # Sauvegarder directement ce qui est reçu (en supposant que c'est complet et correct)
        CONFIG_PATH.write_text(jsonify_safe(data), encoding='utf-8')
        config = AIProjectConfig.from_json(CONFIG_PATH)
        config.to_json(Path("config.json"))
        return jsonify({"message": "Configuration mise à jour avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Helper functions
def config_as_dict():
    """
    Convertir la configuration actuelle en dictionnaire,
    en convertissant récursivement les objets Path en chaînes.
    """
    from dataclasses import asdict
    return convert_paths(asdict(config))


def jsonify_safe(data):
    """
    Retourner une chaîne JSON propre pour stockage dans le fichier.
    """
    import json
    return json.dumps(data, indent=4, ensure_ascii=False)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
