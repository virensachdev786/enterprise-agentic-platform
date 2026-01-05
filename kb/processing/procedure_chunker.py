import json
import re
from pathlib import Path
from typing import Dict, List

def parse_frontmatter(md: str) -> Dict[str, str]:
    """
    Extract YAML frontmatter between --- and --- markers.
    """
    # Standard regex to find content between triple-dashes at the start of a file
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", md, re.S | re.M)
    if not match:
        return {}

    block = match.group(1)
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta

def chunk_procedure(md_path: Path) -> Dict:
    raw = md_path.read_text()
    meta = parse_frontmatter(raw)
    
    # Strip frontmatter from the document body
    body = re.sub(r"^---.*?---\s*", "", raw, flags=re.S | re.M).strip()

    return {
        "id": meta.get("procedure_id", md_path.stem),
        "document": body,
        "metadata": {
            "procedure_id": meta.get("procedure_id"),
            "intent": meta.get("intent"),
            "system": meta.get("system"),
            "execution_mode": meta.get("execution_mode"),
            "confidence_min": float(meta.get("confidence_min", 0.0)),
            "source": "procedure_kb"
        }
    }

def load_and_save_procedures(kb_dir: Path, output_file: Path):
    """
    Loads all .md files, chunks them, and saves to a JSONL file.
    """
    # Ensure the directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    procedures = []
    # Search for all markdown files in the procedures directory
    for md_file in kb_dir.glob("procedures/*.md"):
        procedures.append(chunk_procedure(md_file))
    
    # Write to JSONL (one JSON object per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in procedures:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Successfully processed {len(procedures)} procedures.")
    print(f"Chunks saved to: {output_file}")

# --- EXECUTION ---
# Define your paths
base_dir = Path("/Users/virensachdev/Desktop/enterprise-agentic-platform")
kb_path = base_dir / "kb"
jsonl_output = base_dir / "db/vectorstore/procedure_chunks.jsonl"

if __name__ == "__main__":
    load_and_save_procedures(kb_path, jsonl_output)