import docx
from PyPDF2 import PdfReader
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileScoreRequestSerializer
from scorer.services import ResumeScorer  
from .utils import extract_text 


class ResumeFileScoreView(APIView):
    def post(self, request):
        serializer = FileScoreRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume_file = serializer.validated_data["resume_file"]
        job_desc = serializer.validated_data["job_description"]

        # Extract text
        text = ""
        if resume_file.name.endswith(".pdf"):
            reader = PdfReader(resume_file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif resume_file.name.endswith(".docx"):
            doc = docx.Document(resume_file)
            text = " ".join(p.text for p in doc.paragraphs)
        else:
            text = resume_file.read().decode("utf-8", errors="ignore")

        breakdown = score_resume(text, job_desc)

        # Suggestions
        suggestions = []
        missing_keywords = breakdown.details["content"]["missing"]
        if missing_keywords:
            suggestions.append(f"Add missing keywords: {', '.join(missing_keywords[:10])}...")
        for section, present in breakdown.details["sections"]["details"].items():
            if not present:
                suggestions.append(f"Include a {section.title()} section.")
        if not breakdown.details["formatting"]["has_email"]:
            suggestions.append("Add a professional email address.")
        if not breakdown.details["formatting"]["has_phone"]:
            suggestions.append("Add a phone number.")

        return Response({
            "total": breakdown.total,
            "breakdown": {
                "content_match": breakdown.content_match,
                "section_coverage": breakdown.section_coverage,
                "formatting": breakdown.formatting,
                "readability": breakdown.readability,
            },
            "suggestions": suggestions,
            "details": breakdown.details,
        }, status=status.HTTP_200_OK)
from scorer.services import ResumeScorer

class ResumeFileScoreView(APIView):
    def post(self, request):
        resume_file = request.FILES.get("resume_file")
        job_description = request.data.get("job_description", "")

        resume_text = extract_text(resume_file)  # your existing parser
        scorer = ResumeScorer()
        result = scorer.score(resume_text, job_description)

        return Response(result)
