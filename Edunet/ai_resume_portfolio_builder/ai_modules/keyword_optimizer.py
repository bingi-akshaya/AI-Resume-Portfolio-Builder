import re

# lightweight stopword list adapted from common sources
STOPWORDS = {
    'a','an','and','are','as','at','be','by','for','from','has','he','in','is','it',
    'its','of','on','that','the','to','was','were','will','with','i','you','your',
    'we','our','us','their','they','them','this','these','those','but','or','if',
}


def _tokenize(text):
    # simple word extraction
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def optimize_keywords(resume, job_description):
    """Improve a list of resume lines using keywords from a job description.

    - Extract meaningful words from the description (removing stopwords).
    - Identify which keywords are not already present in the resume.
    - Append a small "ATS Keywords" section listing the missing keywords.

    Parameters
    ----------
    resume : list[str]
        List of lines that make up the current resume content.
    job_description : str
        Text of a job description to pull keywords from.

    Returns
    -------
    list[str]
        A new list of lines with any missing keywords added at the end.
    """

    if not job_description or not resume:
        return resume

    # tokenize and clean the job description without heavy libraries
    tokens = _tokenize(job_description)
    keywords = set(t for t in tokens if t not in STOPWORDS)

    # normalize resume words for comparison
    existing = set()
    for line in resume:
        for w in re.findall(r"\b\w+\b", line.lower()):
            existing.add(w)

    missing = sorted(keywords - existing)
    if not missing:
        return resume

    optimized = list(resume)
    optimized.append("")
    optimized.append("ATS Keywords:")
    for kw in missing:
        optimized.append(f"- {kw}")

    return optimized
