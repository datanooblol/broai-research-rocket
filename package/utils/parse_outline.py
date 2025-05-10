import re

def parse_outline(outline: str):
    sections = []
    current_section = None

    for line in outline.splitlines():
        line = line.strip()
        if line.startswith("## "):
            # Start a new section
            section_title = line[3:].strip()
            current_section = {"section": section_title, "questions": []}
            sections.append(current_section)
        elif (line.startswith("* ") or line.startswith("- ")) and current_section:
            # Add question to the current section
            question = line[2:].strip()
            current_section["questions"].append(question)
            # current_section["questions"].append({"question":question, "urls": []})

    return sections