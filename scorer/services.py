import re
from sklearn.feature_extraction.text import CountVectorizer
from textstat import flesch_reading_ease
from docx import Document
from PyPDF2 import PdfReader


def extract_text(file):
    """Extract text from PDF, DOCX, or TXT resume files."""
    if not file:
        return ""
    name = file.name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(file)
        texts = []
        for page in reader.pages:
            t = page.extract_text() or ""
            if t:
                texts.append(t)
        return "\n".join(texts)
    elif name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".txt"):
        try:
            return file.read().decode("utf-8")
        except Exception:
            try:
                return file.read().decode("latin-1")
            except Exception:
                return ""
    return ""


class ResumeScorer:
    def score(self, resume_text, job_description):
        """Main scoring function that returns total score, breakdown, and suggestions."""
        content_score = self.keyword_match(resume_text, job_description)
        section_score = self.section_coverage(resume_text)
        formatting_score = self.formatting_quality(resume_text)
        readability_score = self.readability_score(resume_text)

        total = round(
            (content_score + section_score + formatting_score + readability_score) / 4,
            2
        )

        return {
            "total": total,
            "breakdown": {
                "content_match": round(content_score, 2),
                "section_coverage": round(section_score, 2),
                "formatting": round(formatting_score, 2),
                "readability": round(readability_score, 2),
            },
            "suggestions": self.generate_suggestions(resume_text, job_description),
        }

    def keyword_match(self, resume, jd):
        """Check how many job description keywords appear in the resume."""
        resume = resume.strip()
        jd = jd.strip()

        if not resume or not jd:
            return 0.0

        vectorizer = CountVectorizer(stop_words="english")

        try:
            jd_words = set(vectorizer.fit([jd]).get_feature_names_out())
            resume_words = set(vectorizer.fit([resume]).get_feature_names_out())
        except ValueError:
            return 0.0

        match = jd_words & resume_words
        return (len(match) / len(jd_words)) * 100 if jd_words else 0.0

    def section_coverage(self, text):
        """Check if key resume sections are present."""
        sections = ["experience", "education", "skills", "summary", "profile"]
        tl = text.lower()
        found = [s for s in sections if s in tl]
        return (len(found) / len(sections)) * 100

    def formatting_quality(self, text):
        """Evaluate formatting quality based on presence of key elements."""
        score = 0
        # Year pattern
        if re.search(r"\b(19|20)\d{2}\b", text):
            score += 20
        # Email
        if re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text):
            score += 20
        # Phone
        if re.search(r"\+?\d[\d\s\-()]{8,}\d", text):
            score += 20
        # Bullets
        if re.search(r"[•\*\-]\s", text):
            score += 20
        # Length
        if len(text.split()) > 200:
            score += 20
        return score

    def readability_score(self, text):
        """Calculate readability using Flesch Reading Ease."""
        try:
            score = flesch_reading_ease(text)
            return max(0, min(100, float(score)))
        except Exception:
            return 50.0

    def generate_suggestions(self, resume, jd):
        """Generate tailored suggestions based on weaknesses and strengths."""
        suggestions = set()

        # Keyword match
        if self.keyword_match(resume, jd) < 30:
            suggestions.add("Add missing keywords from the job description to improve content match.")
            suggestions.add("Use job-specific terms like technologies, tools, and certifications mentioned in the posting.")

        # Section coverage
        missing_sections = []
        for section in ["Experience", "Education", "Skills", "Summary", "Profile"]:
            if section.lower() not in resume.lower():
                missing_sections.append(section)
        if missing_sections:
            suggestions.add(f"Include the following missing sections: {', '.join(missing_sections)}.")
            suggestions.add("Label each section clearly and use ATS-friendly formatting (no tables/columns).")

        # Formatting
        if self.formatting_quality(resume) < 60:
            suggestions.add("Improve formatting: add bullet points, consistent date formats, and contact info (email, phone).")
            suggestions.add("Use clean headings (e.g., 'Experience', 'Education') and simple layout.")

        # Readability
        if self.readability_score(resume) < 60:
            suggestions.add("Simplify language and structure; aim for shorter sentences and active voice.")
            suggestions.add("Break dense text into bullets highlighting impact and results.")

        # Length guidance
        word_count = len(resume.split())
        if word_count < 150:
            suggestions.add("Add more detail to roles: responsibilities, tech stack, and quantifiable achievements.")
        elif word_count > 800:
            suggestions.add("Trim repetitive content; focus on impactful bullet points with measurable outcomes.")

        # Positive reinforcement
        if self.formatting_quality(resume) >= 80:
            suggestions.add("Good formatting: bullets and clear structure are helping ATS parsing.")
        if self.section_coverage(resume) >= 80:
            suggestions.add("Strong section coverage — keep labels consistent and concise.")

        return list(suggestions)
