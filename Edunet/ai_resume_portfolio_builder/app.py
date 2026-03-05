from flask import Flask, render_template, request, send_file
import os

from ai_modules.resume_generator import generate_resume
from ai_modules.portfolio_generator import generate_portfolio
from ai_modules.skill_analyzer import analyze_skills
from ai_modules.keyword_optimizer import optimize_keywords
from ai_modules.job_description_analyzer import analyze_job_description
from ai_modules.resume_scorer import score_resume
from ai_modules.cover_letter_generator import generate_cover_letter
from ai_modules.interview_question_generator import generate_questions
from utils.pdf_generator import generate_pdf
from utils.qr_generator import create_qr

app = Flask(__name__)

RESUME_FOLDER = "generated/resumes"
PORTFOLIO_FOLDER = "generated/portfolios"
QR_FOLDER = "generated/qr"

os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(PORTFOLIO_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# in-memory store for demo purposes
saved_portfolios = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/portfolio/<name>")
def show_portfolio(name):
    data = saved_portfolios.get(name)
    if not data:
        return "Portfolio not found", 404
    return render_template("portfolio.html", portfolio=data)


@app.route("/generate", methods=["POST"])
def generate():

    name = request.form.get("name", "").strip()
    photo = request.form.get("photo", "").strip()
    contact = request.form.get("contact", "").strip()
    summary = request.form.get("summary", "")
    skills = [s.strip() for s in request.form.get("skills", "").split(",") if s.strip()]
    projects = request.form.get("projects", "")
    experience = request.form.get("experience", "")
    education = request.form.get("education", "")
    certifications = request.form.get("certifications", "")
    awards = request.form.get("awards", "")
    languages = request.form.get("languages", "")
    about = request.form.get("about", "")
    job_desc = request.form.get("job_description", "")
    position = request.form.get("position", "")
    company = request.form.get("company", "")

    data = {
        "name": name,
        "photo": photo,
        "contact": contact,
        "summary": summary,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "certifications": certifications,
        "awards": awards,
        "languages": languages,
        "about": about,
    }

    resume_content = generate_resume(data)
    suggestions = analyze_skills(skills)

    # analyze job description and optimize resume if provided
    job_analysis = analyze_job_description(job_desc) if job_desc else {}
    optimized_resume = (
        optimize_keywords(resume_content, job_desc) if job_desc else resume_content
    )
    resume_score = score_resume(optimized_resume)

    # interview questions based on final resume
    interview_questions = generate_questions(optimized_resume)

    # generate pdf from optimized resume (include photo if present)
    filename = f"{RESUME_FOLDER}/{name}_resume.pdf"
    generate_pdf(filename, optimized_resume, photo_url=data.get("photo"))

    # use theme selection if provided
    theme = request.form.get("theme", "default")
    data["theme"] = theme

    portfolio = generate_portfolio(data)
    portfolio["resume_file"] = filename
    saved_portfolios[name] = portfolio

    # generate QR code pointing to the portfolio page
    qr_file = f"{QR_FOLDER}/{name}_qr.png"
    portfolio_url = request.host_url.rstrip("/") + "/portfolio/" + name
    create_qr(portfolio_url, qr_file)

    # optionally generate a cover letter
    cover_letter = None
    if position and company and name:
        cover_letter = generate_cover_letter(name, position, company, highlights=skills[:3])

    return render_template(
        "preview.html",
        resume=optimized_resume,
        original_resume=resume_content,
        portfolio=portfolio,
        suggestions=suggestions,
        job_analysis=job_analysis,
        resume_score=resume_score,
        cover_letter=cover_letter,
        filename=filename,
        qr_file=qr_file,
        interview_questions=interview_questions,
    )


@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)


@app.route("/qr/<filename>")
def serve_qr(filename):
    path = os.path.join(QR_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, mimetype="image/png")
    return "", 404


if __name__ == "__main__":
    app.run(debug=True)