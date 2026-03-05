# AI Resume & Portfolio Builder

This project is a Flask-based web application that helps users quickly generate a professional resume and personal portfolio.

## Core Features

- Resume generator with sections for summary, skills, projects, experience, education, certifications, awards/honors, and languages. Supports an optional profile picture URL.
- Portfolio page creation based on user data.
- PDF export of the resume with styled formatting and bullet points.
- Suggestions for missing skills based on a common skill list.
- Resume preview before downloading.

## Intermediate / AI Features

- **Resume content improvement**: simple sentence rewriting rules make bullet points sound more professional.
- **Skill gap analyzer** suggests additional skills.
- **Job description analyzer** extracts required skills, experience level, and keywords.
- **ATS keyword optimizer** injects relevant keywords from a job description into the resume.
- **Resume scoring** gives a 0–100 score with strengths and improvement suggestions; it now rewards certifications, awards, and languages as well.
- **Cover letter generator** using name, position, and company.
- **Interview question generator** creates basic technical questions from resume lines.

## Advanced Enhancements

- **QR code embedding**: each generated resume PDF includes a QR code linking to the portfolio page.
- **Portfolio themes**: users can choose default, dark, or minimal themes for the portfolio.
- **PDF formatting improvements**: headers, bullets, and spacing make the document look polished.
- **Persistent portfolio route** (`/portfolio/<name>`) with download link for the resume.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   python app.py
   ```
3. Visit `http://127.0.0.1:5000/form` to enter your details.

## Future Ideas

- GitHub project importer
- Voice input for resume creation
- Real-time resume feedback
- LinkedIn profile generator, etc.

