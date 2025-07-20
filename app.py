import json
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Charger le fichier JSON existant ou utiliser les valeurs par défaut
CONFIG_FILE = "config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
else:
    # Générer le JSON si absent
    from generate_config_json import config_dict as config_data

@app.route('/')
def config_page():
    return render_template('config.html', config=config_data)

@app.route('/save_config', methods=['POST'])
def save_config():
    new_config = request.get_json()
    
    # Mettre à jour les valeurs dans config_data
    for section in ['paths', 'data', 'processing', 'model']:
        for key, value in new_config.get(section, {}).items():
            if section == 'model' and key == 'output_paths':
                for path_key, path_value in value.items():
                    config_data[section][key][path_key] = path_value
            else:
                config_data[section][key] = value
    
    # Sauvegarder dans config.json
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    
    return jsonify({"message": "Configuration sauvegardée avec succès !"})

if __name__ == '__main__':
    app.run(debug=True)