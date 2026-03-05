def score_resume(lines):
    """Assign a rudimentary score to a resume represented as a list of lines.

    Returns a dict with the score, a list of strengths and a list of
    suggestions. The algorithm is intentionally simple – it merely looks for
    the presence of certain sections and counts bullet points.
    """
    score = 0
    strengths = []
    suggestions = []

    text = "\n".join(lines).lower()

    if "skills:" in text:
        score += 15
        strengths.append("Includes a skills section")
    else:
        suggestions.append("Add a skills section to highlight your abilities")

    if "projects:" in text or "experience:" in text:
        score += 20
        strengths.append("Contains project/experience details")
    else:
        suggestions.append("Describe at least one project or work experience")

    if "certifications:" in text:
        score += 10
        strengths.append("Lists relevant certifications")

    if "awards" in text:
        score += 10
        strengths.append("Highlights awards or honors")

    if "languages:" in text:
        score += 5
        strengths.append("Specifies languages")

    bullets = [l for l in lines if l.strip().startswith("-")]
    score += min(len(bullets) * 4, 40)
    if len(bullets) >= 5:
        strengths.append("Good number of bullet points")
    else:
        suggestions.append("Add more achievement‑oriented bullet points")

    # length bonus (up to 20 points)
    if len(lines) >= 18:
        score += 20
    else:
        suggestions.append("Consider expanding your resume with more detail")

    score = min(score, 100)
    return {"score": score, "strengths": strengths, "suggestions": suggestions}
