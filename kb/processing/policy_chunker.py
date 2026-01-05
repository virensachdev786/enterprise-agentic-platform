import os
import json
import re
from pathlib import Path

POLICY_DIR = "./kb/policies"
OUTPUT_FILE = "./db/vectorstore/chunks.jsonl"


def read_markdown_files(directory):
    files = []
    for f in os.listdir(directory):
        if f.endswith(".md"):
            path = os.path.join(directory, f)
            with open(path, "r") as file:
                files.append((f.replace(".md", ""), file.read()))
    return files


def extract_policy_title(md_text):
    """
    Extracts the first H1 (# Title)
    """
    match = re.search(r"^# (.+)", md_text, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown Policy"


def split_into_sections(md_text):
    """
    Splits document into {section_title, content} chunks based on H2 headers.
    If document has no H2, returns full document as one chunk.
    """
    sections = re.split(r"(?m)^## ", md_text)

    if len(sections) == 1:
        return [{"section": "General", "content": sections[0]}]

    structured = []
    first_block = sections[0].strip()

    # if content exists before first ## section, keep it as "Overview"
    if first_block.startswith("#"):
        structured.append({"section": "Overview", "content": first_block})

    for sec in sections[1:]:
        lines = sec.splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        structured.append({"section": title, "content": body})

    return structured


def build_chunks():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    files = read_markdown_files(POLICY_DIR)
    output = []

    for file_name, text in files:
        policy_title = extract_policy_title(text)
        sections = split_into_sections(text)

        for idx, sec in enumerate(sections):
            chunk = {
                "id": f"{file_name}_chunk_{idx}",
                "policy_file": file_name,
                "policy_title": policy_title,
                "section": sec["section"],
                "text": sec["content"],
                "metadata": {
                    "type": "policy",
                    "source": "internal_security_policy",
                    "policy_name": policy_title,
                    "section_name": sec["section"],
                    "risk_level": infer_risk_level(policy_title)
                }
            }

            output.append(chunk)

    with open(OUTPUT_FILE, "w") as f:
        for row in output:
            f.write(json.dumps(row) + "\n")

    print(f"Created {len(output)} chunks → {OUTPUT_FILE}")


def infer_risk_level(policy_name):
    """
    Optional smart metadata tagging.
    Makes retrieval more meaningful later.
    """
    high_keywords = ["VIP", "Executive", "Security", "MFA", "Escalation"]
    medium_keywords = ["Eligibility", "Incident"]
    low_keywords = ["Logging"]

    name = policy_name.lower()

    if any(k.lower() in name for k in high_keywords):
        return "HIGH"

    if any(k.lower() in name for k in medium_keywords):
        return "MEDIUM"

    if any(k.lower() in name for k in low_keywords):
        return "LOW"

    return "MEDIUM"


if __name__ == "__main__":
    build_chunks()

