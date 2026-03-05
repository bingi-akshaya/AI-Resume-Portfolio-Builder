import re


def _split_items(field):
    """Split a text field into a list of trimmed items.

    Accepts a newline-, comma- or semicolon-separated string or a list.
    """
    if not field:
        return []
    if isinstance(field, list):
        return [str(x).strip() for x in field if str(x).strip()]
    text = str(field)
    parts = re.split(r"[\n;,]+", text)
    return [p.strip() for p in parts if p.strip()]


def _improve_sentence(sentence):
    sentence = sentence.strip()
    if not sentence:
        return ""

    # very simple rule‑based rewrites to make content sound more professional
    replacements = {
        r"\bworked on\b": "Developed",
        r"\bworked with\b": "Collaborated with",
        r"\bresponsible for\b": "Led",
        r"\butilized\b": "Used",
        r"\bcreated\b": "Developed",
        r"\bhelped\b": "Assisted",
        r"\bbuilt\b": "Constructed",
    }
    for pattern, repl in replacements.items():
        sentence = re.sub(pattern, repl, sentence, flags=re.I)

    # Capitalize first letter and ensure punctuation
    sentence = sentence[0].upper() + sentence[1:]
    if not sentence.endswith("."):
        sentence += "."
    return sentence


def generate_resume(data):
    """Return a list of strings representing the lines of a resume.

    The returned list can be fed directly to :func:`utils.pdf_generator.generate_pdf`.

    Parameters
    ----------
    data : dict
        Dictionary containing keys like ``name``, ``skills``, ``projects``,
        ``experience`` and ``education``. Skills should be a list, other
        fields may be strings or lists.
    """

    lines = []

    name = data.get("name")
    photo = data.get("photo")
    contact = data.get("contact")
    if name:
        lines.append(name.strip())
        if contact:
            lines.append(contact.strip())
        lines.append("")
    # photo handled separately by PDF generator

    # summary/objective
    summary = data.get("summary")
    if summary:
        lines.append("Summary:")
        lines.append(summary.strip())
        lines.append("")

    skills = _split_items(data.get("skills"))
    if skills:
        lines.append("Skills:")
        # skills will be rendered in one line by pdf generator
        for s in skills:
            lines.append(f"- {s}")
        lines.append("")

    projects = _split_items(data.get("projects"))
    if projects:
        lines.append("Projects:")
        for p in projects:
            lines.append(f"- {_improve_sentence(p)}")
        lines.append("")

    experience = _split_items(data.get("experience"))
    if experience:
        lines.append("Experience:")
        for e in experience:
            lines.append(f"- {_improve_sentence(e)}")
        lines.append("")

    education = _split_items(data.get("education"))
    if education:
        lines.append("Education:")
        for e in education:
            lines.append(f"- {e}")
        lines.append("")

    certs = _split_items(data.get("certifications"))
    if certs:
        lines.append("Certifications:")
        for c in certs:
            lines.append(f"- {c}")
        lines.append("")

    awards = _split_items(data.get("awards"))
    if awards:
        lines.append("Awards & Honors:")
        for a in awards:
            lines.append(f"- {a}")
        lines.append("")

    langs = _split_items(data.get("languages"))
    if langs:
        lines.append("Languages:")
        for l in langs:
            lines.append(f"- {l}")
        lines.append("")

    # fallback if nothing provided
    if not lines:
        lines.append("No resume data provided.")

    return lines

