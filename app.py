from flask import Flask, jsonify
import json
import os
import re

app = Flask(__name__)

NOTEBOOK_FILE = "cl3.ipynb"  # Update if filename differs

# Load notebook
with open(NOTEBOOK_FILE, "r") as f:
    nb = json.load(f)

code_map = {}
current_tag = None

# Regex to match tags like '## P1: Title' or '### P2 - something'
tag_regex = re.compile(r'^#+\s*P(\d+)', re.IGNORECASE)

for cell in nb["cells"]:
    if cell["cell_type"] == "markdown":
        for line in cell["source"]:
            match = tag_regex.match(line.strip())
            if match:
                current_tag = f"P{match.group(1)}".upper()
                if current_tag not in code_map:
                    code_map[current_tag] = []  # Initialize list of code blocks
    elif cell["cell_type"] == "code" and current_tag:
        code_map[current_tag].append("".join(cell["source"]))

# Route to return full code (all cells) for a given tag, preserving formatting
@app.route("/code/<tag>")
def get_code(tag):
    tag = tag.upper()
    if tag in code_map:
        full_code = "\n\n".join(code_map[tag])  # Separate code blocks clearly
        return jsonify({tag: full_code})
    else:
        return jsonify({"error": f"No code found for tag: {tag}"}), 404

# Debug route to list all detected tags
@app.route("/tags")
def list_tags():
    return jsonify(sorted(code_map.keys()))

# Start the app on correct host/port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
