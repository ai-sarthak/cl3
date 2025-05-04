from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import json

app = FastAPI()

# Load notebook once
with open("cl3.ipynb", "r", encoding="utf-8") as f:
    notebook = json.load(f)

@app.get("/code/{section_id}", response_class=PlainTextResponse)
def get_code(section_id: str):
    found_section = False
    code_lines = []
    section_header = f"## {section_id}"

    for cell in notebook.get("cells", []):
        if cell["cell_type"] == "markdown":
            # Start capturing when header matches
            if any(section_header in line for line in cell.get("source", [])):
                found_section = True
                continue
            # Stop when we hit the next ## section
            if found_section and any(line.startswith("## ") for line in cell.get("source", [])):
                break
        elif cell["cell_type"] == "code" and found_section:
            code_lines.append("".join(cell.get("source", [])))

    if not code_lines:
        raise HTTPException(status_code=404, detail="Section not found or no code under this section.")

    return "\n".join(code_lines)
