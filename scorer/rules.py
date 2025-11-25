DEFAULT_WEIGHTS = {
    "content_match": 0.50,
    "section_coverage": 0.25,
    "formatting": 0.15,
    "readability": 0.10,
}

# Default sections ATS/lookalike tools expect
REQUIRED_SECTIONS = ["experience", "work experience", "employment",
                     "education", "skills", "summary", "profile"]

# Common ATS-friendly fonts
ATS_FONTS = {"arial", "calibri", "helvetica", "georgia", "garamond", "times new roman", "verdana"}
