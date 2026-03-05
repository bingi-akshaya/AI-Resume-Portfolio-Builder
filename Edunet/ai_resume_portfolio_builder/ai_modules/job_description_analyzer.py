import re
from collections import Counter

# lightweight stopword set (same as keyword_optimizer)
STOPWORDS = {
    'a','an','and','are','as','at','be','by','for','from','has','he','in','is','it',
    'its','of','on','that','the','to','was','were','will','with','i','you','your',
    'we','our','us','their','they','them','this','these','those','but','or','if',
}

# use the same skill list as skill_analyzer to guess required skills
COMMON_SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Data Visualization",
    "Django",
    "Flask",
    "React",
    "Node.js",
    "Git",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "Linux",
]


def analyze_job_description(text):
    """Extract high‑level information from a job description string.

    Returns a dict containing:

    * ``required_skills`` – intersection with a known skill list
    * ``experience_level`` – simple categorization from years mentioned
    * ``keywords`` – most frequent non‑stopword tokens
    """
    if not text:
        return {}

    tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    filtered = [t for t in tokens if t not in STOPWORDS]

    freq = Counter(filtered)
    keywords = [word for word, _ in freq.most_common(15)]

    req_skills = []
    lowered = set(keywords)
    for skill in COMMON_SKILLS:
        if skill.lower() in lowered:
            req_skills.append(skill)

    exp_level = "Not specified"
    m = re.search(r"(\d+)\s+years?", text, re.I)
    if m:
        yrs = int(m.group(1))
        if yrs < 2:
            exp_level = "Entry"
        elif yrs < 5:
            exp_level = "Mid"
        else:
            exp_level = "Senior"

    return {
        "required_skills": req_skills,
        "experience_level": exp_level,
        "keywords": keywords,
    }
