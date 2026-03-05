def generate_cover_letter(name, position, company, highlights=None):
    """Return a basic cover letter text using provided details.

    ``highlights`` can be a list of accomplishments or skills to call out.
    """
    lines = []
    lines.append(f"Dear Hiring Manager at {company},")
    lines.append("")
    lines.append(f"My name is {name} and I am excited to apply for the {position} role.")
    if highlights:
        lines.append("")
        lines.append("In particular, I would like to highlight:")
        for h in highlights:
            lines.append(f"- {h}")
    lines.append("")
    lines.append("Thank you for considering my application. I look forward to the opportunity to contribute to your team.")
    lines.append("")
    lines.append("Sincerely,")
    lines.append(name)
    return "\n".join(lines)
