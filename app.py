from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load the notebook
with open("cl3.ipynb") as f:
    nb = json.load(f)

# Map tags like "P1", "P2" to the next code block
code_map = {}
last_tag = None

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        for line in cell['source']:
            line = line.strip()
            if line.startswith("P") and line[1:].isdigit():
                last_tag = line
    elif cell['cell_type'] == 'code' and last_tag:
        code_map[last_tag] = "".join(cell['source'])
        last_tag = None

@app.route('/get/<tag>')
def get_code(tag):
    tag = tag.upper()
    code = code_map.get(tag)
    if code:
        return jsonify({tag: code})
    else:
        return jsonify({"error": f"No code found for tag: {tag}"}), 404
