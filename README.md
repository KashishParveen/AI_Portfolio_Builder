---
title: AI Portfolio Builder
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---
# PortfolioAI — AI Resume & Portfolio Builder
### IBM SkillsBuild × Edunet Foundation Internship Project

---

## ✦ Features

| Feature | Description |
|---|---|
| 📄 Resume Generator | ATS-optimized, formatted resume |
| ✉️ Cover Letter | Role-specific professional letter |
| 🌐 Portfolio Bio | 3-paragraph first-person bio |
| 💼 LinkedIn Summary | Ready-to-paste About section |
| 🏷️ ATS Keywords | Keywords extracted from your resume |
| 💡 AI Tips | 5 personalized improvement tips |
| ✨ Resume Improver | AI rewrites your resume with a focus area |
| 📊 ATS Score Checker | Match score vs any job description |
| 🎯 Job Tailor | Rewrites resume for a specific job post |
| 🎤 Interview Prep | AI Q&A based on your resume + role |
| 📈 Skill Gap Analyser | Missing skills + learning path |
| ⬇️ DOCX Export | Formatted Word document |
| ⬇️ PDF Export | Print-ready PDF |

---

## 📁 Project Structure

```
PortfolioAI/
├── app.py                  ← Flask server + all API routes
├── requirements.txt        ← Python dependencies
├── Procfile                ← For Render/Heroku deployment
├── .env.example            ← Template for your API keys
├── .gitignore              ← Files to exclude from Git
├── templates/
│   └── index.html          ← Full responsive frontend (HTML/CSS/JS)
└── utils/
    ├── __init__.py
    ├── llm.py              ← HuggingFace API caller
    ├── generate_docx.py    ← Word document generator
    └── generate_pdf.py     ← PDF generator
```

---

## 🔑 STEP 1 — Get Your API Key

1. Go to **https://huggingface.co/settings/tokens**
2. Click **"New token"**
3. Name: `portfolioai` | Type: `Read`
4. Click **Generate** → Copy the token (starts with `hf_`)

---

## ⚙️ STEP 2 — Set Up Your Environment

### Option A — .env file (Recommended for local dev)
1. In the project folder, find `.env.example`
2. **Copy** it and rename the copy to `.env`
3. Open `.env` and replace the placeholder:
   ```
   HF_TOKEN=hf_your_actual_token_here
   ```

### Option B — Terminal (quick method)
```bash
# Windows PowerShell
$env:HF_TOKEN = "hf_your_token_here"

# Windows CMD
set HF_TOKEN=hf_your_token_here

# Mac / Linux
export HF_TOKEN=hf_your_token_here
```

### Option C — Directly in llm.py (NOT for GitHub)
In `utils/llm.py`, line 16, replace:
```python
HF_TOKEN = os.getenv("HF_TOKEN", "")
```
with:
```python
HF_TOKEN = "hf_your_actual_token_here"
```
⚠️ **Never push this to GitHub!**

---

## 💻 STEP 3 — Run Locally (VS Code)

```bash
# 1. Open terminal in VS Code (Ctrl + `)

# 2. Navigate to project folder
cd PortfolioAI

# 3. (Optional) Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py

# 6. Open in browser
# → http://localhost:5000
```

---

## 🌐 STEP 4A — Deploy to Render (FREE, recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "PortfolioAI - IBM SkillsBuild project"
   git remote add origin https://github.com/YOUR_USERNAME/portfolioai.git
   git push -u origin main
   ```
   ⚠️ Make sure `.env` is in `.gitignore` before pushing!

2. **Go to https://render.com** → Sign up free

3. Click **New → Web Service**

4. **Connect your GitHub repo**

5. Fill in settings:
   ```
   Name:          portfolioai
   Runtime:       Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

6. **Add Environment Variable:**
   - Key: `HF_TOKEN`
   - Value: `hf_your_token_here`

7. Click **"Create Web Service"**

8. Wait ~3 minutes → Your app is live at:
   `https://portfolioai.onrender.com`

> ⚠️ Free tier sleeps after 15 min of inactivity. First load may take ~30s.

---

## 🚂 STEP 4B — Deploy to Railway (Alternative)

1. Go to **https://railway.app** → Sign in with GitHub
2. Click **New Project → Deploy from GitHub Repo**
3. Select your repo
4. Go to **Variables tab** → Add:
   - `HF_TOKEN` = `hf_your_token_here`
5. Railway auto-detects Flask and deploys!
6. Get your public URL from the **Settings → Domains** tab

---

## ☁️ STEP 4C — Deploy to Vercel

Create `vercel.json` in the root:
```json
{
  "builds": [{"src": "app.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "app.py"}]
}
```
Then:
```bash
npm i -g vercel
vercel --prod
```

---

## 🔄 Changing the AI Model

In `.env`, change:
```
HF_MODEL=openbmb/MiniCPM-SALA
```
To any other HuggingFace text-generation model, e.g.:
- `mistralai/Mistral-7B-Instruct-v0.3`
- `meta-llama/Llama-3.2-3B-Instruct`
- `google/gemma-2-2b-it`

---

## 🐞 Troubleshooting

| Problem | Solution |
|---|---|
| `HF_TOKEN not set` | Check your .env file is in the right folder |
| `401 Unauthorized` | Your token is wrong or expired — regenerate it |
| `Timeout error` | Model is loading (~30s). Try again |
| `JSON parse error` | Model returned garbled text. Try a different model |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Port already in use | Change port in app.py: `app.run(port=5001)` |

---

Built with ❤️ as part of **IBM SkillsBuild × Edunet Foundation AI Internship**
