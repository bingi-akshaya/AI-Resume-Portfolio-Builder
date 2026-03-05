def generate_questions(resume_lines):
    """Create a few simple interview questions based on resume lines.

    The implementation looks for project and experience lines and turns them
    into questions by prefixing with "Explain" or "Describe".
    """
    questions = []
    for line in resume_lines:
        if line.startswith("- "):
            text = line[2:]
            if "project" in text.lower():
                questions.append(f"Explain the {text}")
            elif any(word in text.lower() for word in ("developed","built","led")):
                questions.append(f"Describe how you {text}")
    # always include a generic question
    questions.append("What programming languages are you most comfortable with?")
    return questions