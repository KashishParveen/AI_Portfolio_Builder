from flask import Flask, render_template, request, jsonify, send_file, session
import os, json, re, tempfile
from utils.llm import generate_text
from utils.generate_docx import create_docx
from utils.generate_pdf  import create_pdf

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "portfolioai-secret-2024")


# ─── helpers ────────────────────────────────────────────────────────────────
def clean_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*",     "", raw)
    raw = re.sub(r"\s*```$",     "", raw)
    return json.loads(raw.strip())


def build_profile_text(d: dict) -> str:
    edu  = "\n".join(f"- {e['degree']} at {e['school']} ({e['year']})" + (f" | {e['score']}" if e.get("score") else "")
                     for e in d.get("edu", []))
    exp  = "\n".join(f"- {e['title']} @ {e['org']} [{e['period']}]: {e['details']}"
                     for e in d.get("exp", []))
    proj = "\n".join(f"- {p['name']} ({p['tech']}): {p['about']}"
                     for p in d.get("proj", []))
    return f"""
Name: {d.get('name')} | Email: {d.get('email')} | Phone: {d.get('phone')} | Location: {d.get('location')}
LinkedIn: {d.get('linkedin')} | GitHub: {d.get('github')} | Website: {d.get('website')}
Target Role: {d.get('role')} | Headline: {d.get('headline')}
EDUCATION:\n{edu}
EXPERIENCE:\n{exp}
PROJECTS:\n{proj}
SKILLS: {d.get('skills')}
CERTIFICATIONS: {d.get('certs')}
EXTRA: {d.get('extra')}""".strip()


# ─── Routes ─────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    d = request.get_json()
    profile = build_profile_text(d)
    prompt = f"""You are a professional resume writer and career coach.
Generate polished career documents for this candidate.
Return ONLY raw JSON — no markdown, no backticks.

CANDIDATE PROFILE:
{profile}

Return exactly this JSON structure:
{{
  "resume":       "full ATS-optimized resume (use \\n for newlines)",
  "coverLetter":  "professional cover letter (use \\n for newlines)",
  "portfolioBio": "3-paragraph first-person bio (use \\n for newlines)",
  "linkedinSummary": "LinkedIn About section (3-4 sentences, punchy)",
  "tips":         ["tip1","tip2","tip3","tip4","tip5"],
  "keywords":     ["kw1","kw2","kw3","kw4","kw5","kw6","kw7","kw8"]
}}"""
    try:
        result = clean_json(generate_text(prompt, 1400))
        session["last_resume"] = result.get("resume", "")
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/improve", methods=["POST"])
def improve():
    """AI-powered resume improvement suggestions."""
    d      = request.get_json()
    resume = d.get("resume", "")
    focus  = d.get("focus", "overall")
    prompt = f"""You are a resume expert. Improve this resume focusing on: {focus}
Return ONLY raw JSON:
{{"improved": "full improved resume text", "changes": ["change1","change2","change3","change4","change5"]}}

RESUME:
{resume}"""
    try:
        result = clean_json(generate_text(prompt, 1200))
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/ats-score", methods=["POST"])
def ats_score():
    d       = request.get_json()
    resume  = d.get("resume", "")
    job_desc= d.get("jobDesc", "")
    prompt = f"""You are an ATS expert. Analyse this resume vs job description.
Return ONLY raw JSON:
{{
  "score": <0-100>,
  "grade": "<A/B/C/D/F>",
  "matched_keywords": ["kw1","kw2","kw3","kw4","kw5"],
  "missing_keywords": ["kw1","kw2","kw3","kw4","kw5"],
  "suggestions": ["suggestion1","suggestion2","suggestion3","suggestion4"],
  "section_scores": {{"experience": 85, "skills": 70, "education": 90, "format": 80}}
}}

RESUME:\n{resume}\n\nJOB DESCRIPTION:\n{job_desc}"""
    try:
        result = clean_json(generate_text(prompt, 700))
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/job-match", methods=["POST"])
def job_match():
    """Tailor resume to a specific job posting."""
    d       = request.get_json()
    resume  = d.get("resume", "")
    job     = d.get("jobDesc", "")
    prompt = f"""Tailor this resume specifically for the given job description.
Return ONLY raw JSON:
{{"tailored_resume": "tailored resume text", "cover_letter": "tailored cover letter", "match_tips": ["tip1","tip2","tip3"]}}

RESUME:\n{resume}\n\nJOB:\n{job}"""
    try:
        result = clean_json(generate_text(prompt, 1200))
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/interview-prep", methods=["POST"])
def interview_prep():
    """Generate interview Q&A based on resume + role."""
    d      = request.get_json()
    resume = d.get("resume", "")
    role   = d.get("role", "Software Developer")
    prompt = f"""Generate realistic interview questions and model answers for this candidate applying for {role}.
Return ONLY raw JSON:
{{
  "technical":   [{{"q":"question","a":"answer"}}, {{"q":"question","a":"answer"}}, {{"q":"question","a":"answer"}}],
  "behavioral":  [{{"q":"question","a":"answer"}}, {{"q":"question","a":"answer"}}, {{"q":"question","a":"answer"}}],
  "hr":          [{{"q":"question","a":"answer"}}, {{"q":"question","a":"answer"}}],
  "tips": ["interview tip1","interview tip2","interview tip3"]
}}

RESUME:\n{resume}"""
    try:
        result = clean_json(generate_text(prompt, 1000))
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/skill-gap", methods=["POST"])
def skill_gap():
    """Identify skill gaps for a target role."""
    d       = request.get_json()
    skills  = d.get("skills", "")
    role    = d.get("role", "")
    prompt = f"""Analyse skill gaps for someone targeting '{role}' with these skills: {skills}
Return ONLY raw JSON:
{{
  "have": ["skill1","skill2","skill3","skill4"],
  "missing": ["skill1","skill2","skill3","skill4"],
  "learning_path": [{{"skill":"skill name","resource":"free resource URL or platform","time":"est. time"}}],
  "priority": "which skill to learn first and why"
}}"""
    try:
        result = clean_json(generate_text(prompt, 700))
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/download/docx", methods=["POST"])
def download_docx():
    d    = request.get_json()
    path = create_docx(d)
    return send_file(path, as_attachment=True, download_name="resume.docx",
                     mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    d    = request.get_json()
    path = create_pdf(d)
    return send_file(path, as_attachment=True, download_name="resume.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    print("\n  PortfolioAI v3  →  http://localhost:5000\n")
    app.run(debug=True, port=5000)
