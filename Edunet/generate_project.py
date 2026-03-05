import os

project_name = "ai_resume_portfolio_builder"

folders = [
    "static/css",
    "static/js",
    "static/images",
    "templates",
    "generated/resumes",
    "generated/portfolios",
    "ai_modules",
    "utils",
    "data"
]

files = {

# Main app
"app.py": """from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
""",

# Requirements
"requirements.txt": """flask
reportlab
nltk
scikit-learn
""",

# HTML templates
"templates/index.html": "<h1>AI Resume & Portfolio Builder</h1>",
"templates/form.html": "<h2>Enter Your Details</h2>",
"templates/preview.html": "<h2>Resume Preview</h2>",
"templates/portfolio.html": "<h2>Your Portfolio</h2>",
"templates/resume_template.html": "<h2>Resume Template</h2>",

# CSS
"static/css/style.css": """body{
font-family: Arial;
background:#f4f4f4;
}
""",

# JS
"static/js/script.js": """console.log("AI Resume Builder Loaded");""",

# AI Modules

"ai_modules/resume_generator.py": '''def generate_resume(data):
    """
    Generate professional resume content
    """
    resume = {
        "name": data.get("name"),
        "skills": data.get("skills"),
        "projects": data.get("projects")
    }
    return resume
''',

"ai_modules/portfolio_generator.py": '''def generate_portfolio(user_data):
    """
    Generate portfolio website content
    """
    portfolio = {
        "name": user_data.get("name"),
        "projects": user_data.get("projects")
    }
    return portfolio
''',

"ai_modules/skill_analyzer.py": '''def analyze_skills(skills):
    """
    Suggest missing skills
    """
    recommended = ["Machine Learning", "SQL", "Data Visualization"]
    return recommended
''',

"ai_modules/keyword_optimizer.py": '''def optimize_keywords(resume, job_description):
    """
    Improve resume keywords for ATS
    """
    optimized_resume = resume
    return optimized_resume
''',

# Utils

"utils/pdf_generator.py": '''from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, content):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(filename)
    elements = []

    for line in content:
        elements.append(Paragraph(line, styles["Normal"]))

    pdf.build(elements)
''',

"utils/file_handler.py": '''import os

def save_file(path, content):
    with open(path,"w") as f:
        f.write(content)
''',

# Dataset folder placeholder
"data/sample_users.json": "{}"

}

def create_project():
    print("Creating AI Resume Builder project structure...\\n")

    os.makedirs(project_name, exist_ok=True)

    for folder in folders:
        path = os.path.join(project_name, folder)
        os.makedirs(path, exist_ok=True)
        print("Created folder:", path)

    for file_path, content in files.items():
        full_path = os.path.join(project_name, file_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        print("Created file:", full_path)

    print("\\nProject setup complete!")

if __name__ == "__main__":
    create_project()