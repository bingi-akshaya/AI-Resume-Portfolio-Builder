
# simple list of common skills – in a real application this might come
# from a database or external resource.
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

def analyze_skills(skills):
    """Return a list of recommended skills that are not already listed.

    Parameters
    ----------
    skills : list[str]
        Skills that the user has entered.

    Returns
    -------
    list[str]
        Suggested skills to add.
    """

    if not skills:
        return COMMON_SKILLS[:6]

    cleaned = {s.strip().lower() for s in skills if s}
    missing = [s for s in COMMON_SKILLS if s.lower() not in cleaned]
    return missing[:6]  # only suggest a handful at a time

