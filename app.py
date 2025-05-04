from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load notebook
with open("cl3.ipynb") as f:
    nb = json.load(f)

# Map markdown tags like P1, P2 to the code block that follows
code_map = {}
last_tag = None

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        for line in cell['source']:
            line = line.strip()
            if line.startswith("## P") and line[1:].isdigit():
                last_tag = line
    elif cell['cell_type'] == 'code' and last_tag:
        code_map[last_tag] = "".join(cell['source'])
        last_tag = None

@app.route('/code/<tag>')
def get_code(tag):
    tag = tag.upper()
    code = code_map.get(tag)
    if code:
        return jsonify({tag: code})
    else:
        return jsonify({"error": f"No code found for tag: {tag}"}), 404

# 👇 THIS PART IS THE FIX
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
