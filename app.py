from flask import Flask, jsonify
import json
import os
import re

app = Flask(__name__)

# Load notebook file
NOTEBOOK_FILE = "cl3.ipynb"  # 🔁 Update if your filename is different

with open(NOTEBOOK_FILE, "r") as f:
    nb = json.load(f)

code_map = {}
last_tag = None

# Extract tags like P1, P2 from markdown headings
for cell in nb["cells"]:
    if cell["cell_type"] == "markdown":
        for line in cell["source"]:
            line = line.strip()
            match = re.match(r'^#+\s*P(\d+)', line, re.IGNORECASE)
            if match:
                last_tag = f"P{match.group(1)}".upper()
    elif cell["cell_type"] == "code" and last_tag:
        code_map[last_tag] = "".join(cell["source"])
        last_tag = None

# Endpoint to get code by tag
@app.route("/code/<tag>")
def get_code(tag):
    tag = tag.upper()
    code = code_map.get(tag)
    if code:
        return jsonify({tag: code})
    else:
        return jsonify({"error": f"No code found for tag: {tag}"}), 404

# Debug route to list all available tags
@app.route("/tags")
def list_tags():
    return jsonify(sorted(code_map.keys()))

# Run the app with Render-compatible settings
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
