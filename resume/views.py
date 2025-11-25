import json
from django.shortcuts import render,get_object_or_404, redirect
from .models import Resume
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string
from weasyprint import HTML
from .models import Resume1
from .models import Resume2
from .models import Resume3
from .models import Resume4
from .models import Resume5
from .models import JobRole,UserPreference

def landing_page(request):
    return render(request, 'index.html')
def front_page(request):
    return render(request, 'resume/home.html')
def resume_form(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        job_pref = request.POST.get('job_pref', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        summary = request.POST.get('summary', '')
        college_name = request.POST.get('college_name', '')
        degree = request.POST.get('degree', '')
        cgpa = request.POST.get('cgpa', '')
        school_10 = request.POST.get('school_10', '')
        year_10 = request.POST.get('year_10', '')
        percentage_10 = request.POST.get('percentage_10', '')
        school_12 = request.POST.get('school_12', '')
        year_12 = request.POST.get('year_12', '')
        percentage_12 = request.POST.get('percentage_12', '')
        skills = request.POST.get('skills', '')
        languages = request.POST.get('languages', '')
        certificates = request.POST.get('certificates', '')
        projects = request.POST.get('projects', '')
        accomplishments = request.POST.get('accomplishments', '')
        experience = request.POST.get('experience', '')
        resume = Resume.objects.create(
            full_name=full_name, job_pref=job_pref, email=email, phone=phone, city=city,
            summary=summary, college_name=college_name, degree=degree, cgpa=cgpa,
            school_10=school_10, year_10=year_10, percentage_10=percentage_10,
            school_12=school_12, year_12=year_12, percentage_12=percentage_12,
            skills=skills, languages=languages, certificates=certificates,
            projects=projects, accomplishments=accomplishments, experience=experience
        )
        return redirect('resume_detail', resume_id=resume.id)
    return render(request, 'resume/details.html')
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    for field in ['skills', 'languages', 'certificates', 'projects', 'accomplishments', 'experience']:
        value = getattr(resume, field, '')
        if value:
            formatted_value = "\n".join([item.strip() for item in value.split(",")])
            setattr(resume, field, formatted_value)
    return render(request, 'resume/login.html', {'resume': resume})
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'resume/login.html', {'error': 'Invalid username or password'})
    return render(request, 'resume/login.html')
def signup_view(request):
    print(">>> METHOD:", request.method)
    print(">>> POST DATA:", request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            return render(request, 'resume/signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'resume/signup.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'resume/signup.html', {'error': 'Email already registered'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'resume/signup.html')
def logout_view(request):
    logout(request)
    return redirect('login')
def home(request):
    return render(request, 'resume/password_all.html')
@login_required
def dashboard_view(request):
    """Dashboard showing all resumes for the logged-in user."""
    resumes = Resume.objects.filter(user=request.user).order_by('-id')
    return render(request, 'resume/dashboard.html', {'resumes': resumes})
def about_view(request):
    return render(request, 'resume/about.html')
def help_view(request):
    return render(request, 'resume/help.html')
def complaint_view(request):
    return render(request, 'resume/complaint.html')
def privacy_policy_view(request):
    return render(request, 'resume/privacy_policy.html')
def terms_view(request):
    return render(request, 'resume/terms_and_conditions.html')
def safety_tips_view(request):
    return render(request, 'resume/safety_tips.html')
@login_required
def preferences(request):
    all_roles = JobRole.objects.all()
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        selected_role_ids = request.POST.getlist('selected_roles[]')
        user_pref.job_roles.set(selected_role_ids)
        return redirect('preferences')  
    selected_roles = user_pref.job_roles.all()
    return render(request, 'resume/preferences.html', {
        'all_roles': all_roles,
        'selected_roles': selected_roles
    })
@login_required
def add_job_role(request):
    if request.method == 'POST':
        role_name = request.POST.get('name', '').strip()
        if role_name:
            role, created = JobRole.objects.get_or_create(name=role_name)
            if created:
                return JsonResponse({'status': 'success', 'message': f'Added job role: {role.name}', 'id': role.id})
            else:
                return JsonResponse({'status': 'error', 'message': 'Role already exists'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Role name missing'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
@login_required
def delete_job_role(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')
        if role_id:
            role = get_object_or_404(JobRole, id=role_id)
            role.delete()
            return JsonResponse({'status': 'success', 'message': f'Deleted job role with id {role_id}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing role id'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
@login_required
def resume_form1(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_summary = request.POST.get('profile_summary')
        skills = request.POST.get('skills')
        languages = request.POST.get('languages')
        references = request.POST.get('references')

        # Experience and Education as plain text
        experience = request.POST.get('experience',"")
        education = request.POST.get('education',"")

        resume = Resume1.objects.create(
            full_name=full_name,
            job_title=job_title,
            email=email,
            phone=phone,
            address=address,
            profile_summary=profile_summary,
            skills=skills,
            languages=languages,
            references=references,
            work_experience=experience,
            education=education,
            user=request.user
        )

        return redirect('resume_display1', resume_id=resume.id)

    return render(request, 'resume/resume_form1.html')

def resume_display1(request, resume_id):
    resume = get_object_or_404(Resume1, id=resume_id)

    def to_list(text):
        if not text:
            return []
        items = []
        for item in text.replace('\r', '').replace(',', '\n').splitlines():
            item = item.strip()
            if item:
                items.append(item)
        return items

    skills_list = to_list(getattr(resume, 'skills', '') or '')
    languages_list = to_list(getattr(resume, 'languages', '') or '')
    references_list = to_list(getattr(resume, 'references', '') or '')
    experience_list = to_list(getattr(resume, 'work_experience', '') or '')
    education_list = to_list(getattr(resume, 'education', '') or '')

    return render(request, 'resume/resume_display1.html', {
        "resume": resume,
        "skills_list": skills_list,
        "languages_list": languages_list,
        "references_list": references_list,
        "experience_list": experience_list,
        "education_list": education_list,
    })
def download_resume_pdf1(request, resume_id):
    resume = get_object_or_404(Resume1, id=resume_id)

    def split_text(text):
        if not text:
            return []
        return [item.strip() for item in text.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    skills_list = split_text(resume.skills)
    languages_list = split_text(resume.languages)
    references_list = split_text(resume.references)
    experience_list = split_text(resume.work_experience)
    education_list = split_text(resume.education)

    template_path = 'resume/download_resume_pdf1.html'
    context = {
        'resume': resume,
        'skills_list': skills_list,
        'languages_list': languages_list,
        'references_list': references_list,
        'experience_list': experience_list,
        'education_list': education_list,
    }

    template = get_template(template_path)
    html_content = template.render(context)
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'
    return response

@login_required
def resume_form2(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        about_me = request.POST.get('about_me')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        education = request.POST.get('education')
        profile_photo = request.FILES.get('profile_photo')
        

        resume = Resume2.objects.create(
            full_name=full_name,
            job_title=job_title,
            phone=phone,
            email=email,
            about_me=about_me,
            work_experience=experience,
            skills=skills,
            education=education,
            profile_photo=profile_photo,
            user=request.user 
        )
        return redirect('resume_display2', resume_id=resume.id)
    
    return render(request, 'resume/resume_form2.html')


def resume_display2(request, resume_id):
    resume = get_object_or_404(Resume2, id=resume_id)

    # Create clean lists splitting on commas and line breaks
    def to_list(text):
        if not text:
            return []
        # normalize CRLF and replace commas with newline, then splitlines
        items = []
        for item in text.replace('\r', '').replace(',', '\n').splitlines():
            item = item.strip()
            if item:
                items.append(item)
        return items

    experience_list = to_list(getattr(resume, 'work_experience', '') or '')
    skills_list = to_list(getattr(resume, 'skills', '') or '')
    education_list = to_list(getattr(resume, 'education', '') or '')

    context = {
        'resume': resume,
        'experience_list': experience_list,
        'skills_list': skills_list,
        'education_list': education_list,
    }

    return render(request, 'resume/resume_display2.html', context)


def download_resume_pdf2(request, resume_id):
    # Fetch the resume object
    resume = get_object_or_404(Resume2, id=resume_id)

    # Split the text fields by commas or line breaks
    experience_list = []
    if resume.work_experience:
        for exp in resume.work_experience.replace('\r', '').split(','):
            exp = exp.strip()
            if exp:
                experience_list.append(exp)

    skills_list = []
    if resume.skills:
        for skill in resume.skills.replace('\r', '').split(','):
            skill = skill.strip()
            if skill:
                skills_list.append(skill)

    education_list = []
    if resume.education:
        for edu in resume.education.replace('\r', '').split(','):
            edu = edu.strip()
            if edu:
                education_list.append(edu)

    # Load your clean styled template
    template_path = 'resume/download_resume_pdf2.html'

    context = {
        'resume': resume,
        'experience_list': experience_list,
        'skills_list': skills_list,
        'education_list': education_list,
    }

    # Render HTML content
    template = get_template(template_path)
    html_content = template.render(context)

    # Generate PDF using WeasyPrint
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()

    # Send as downloadable file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'

    return response
@login_required
def resume_form3(request):
    if request.method == 'POST':
        resume = Resume3.objects.create(
            full_name=request.POST.get('full_name'),
            job_title=request.POST.get('job_title'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            about=request.POST.get('about'),
            work_experience=request.POST.get('work_experience'),
            education=request.POST.get('education'),
            skills=request.POST.get('skills'),
            languages=request.POST.get('languages'),
            references=request.POST.get('references'),
            profile_image=request.FILES.get('profile_image'),
            user=request.user 
        )
        return redirect('resume_display3', resume_id=resume.id)
    return render(request, 'resume/resume_form3.html')
def resume_display3(request, resume_id):
    resume = get_object_or_404(Resume3, id=resume_id)
    skills_list = [s.strip() for s in resume.skills.replace('\n', ',').split(',') if s.strip()] if resume.skills else []
    experience_list = [e.strip() for e in resume.work_experience.replace('\n', ',').split(',') if e.strip()] if resume.work_experience else []
    education_list = [e.strip() for e in resume.education.replace('\n', ',').split(',') if e.strip()] if resume.education else []
    languages_list = [l.strip() for l in resume.languages.replace('\n', ',').split(',') if l.strip()] if resume.languages else []
    references_list = [r.strip() for r in resume.references.replace('\n', ',').split(',') if r.strip()] if resume.references else []
    context = {
        'resume': resume,
        'skills_list': skills_list,
        'experience_list': experience_list,
        'education_list': education_list,
        'languages_list': languages_list,
        'references_list': references_list,
    }
    return render(request, 'resume/resume_display3.html', context)
def download_resume_pdf3(request, resume_id):
    resume = get_object_or_404(Resume3, id=resume_id)

    # Helper to split text into list
    def split_text(text):
        if not text:
            return []
        return [item.strip() for item in text.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    skills_list = split_text(resume.skills)
    experience_list = split_text(resume.work_experience)
    education_list = split_text(resume.education)
    languages_list = split_text(resume.languages)
    references_list = split_text(resume.references)

    template_path = 'resume/download_resume_pdf3.html'
    context = {
        'resume': resume,
        'skills_list': skills_list,
        'experience_list': experience_list,
        'education_list': education_list,
        'languages_list': languages_list,
        'references_list': references_list,
    }

    # Render HTML to string
    template = get_template(template_path)
    html_content = template.render(context)

    # Generate PDF using WeasyPrint (returns bytes directly)
    pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri('/')).write_pdf()

    # Return as downloadable response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
    return response
@login_required
def resume_form4(request):
    if request.method == 'POST':
        data = {field: request.POST.get(field, '') for field in [
            'full_name', 'job_title', 'address', 'email', 'website', 'phone',
            'profile_summary',   # ✅ added
            'technical_skills', 'projects', 'education', 'work_experience', 'achievements'
        ]}
        resume = Resume4.objects.create(user=request.user, **data) 
        return redirect('resume_display4', resume_id=resume.id)  
    return render(request, 'resume/resume_form4.html')
@login_required
def resume_display4(request, resume_id):
    resume = get_object_or_404(Resume4, id=resume_id)

    def split_field(value):
        if not value:
            return []
        return [item.strip() for item in value.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    context = {
        'resume': resume,
        'profile_summary': resume.profile_summary,   # ✅ added
        'technical_skills': split_field(resume.technical_skills),
        'projects': split_field(resume.projects),
        'experience_list': split_field(resume.work_experience),
        'education_list': split_field(resume.education),
        'achievements_list': split_field(resume.achievements),
    }

    return render(request, 'resume/resume_display4.html', context)
def download_resume_pdf4(request, resume_id):
    resume = get_object_or_404(Resume4, id=resume_id)

    def split_field(value):
        if not value:
            return []
        return [item.strip() for item in value.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    context = {
        'resume': resume,
        'profile_summary': resume.profile_summary,   # ✅ added
        'technical_skills': split_field(resume.technical_skills),
        'projects': split_field(resume.projects),
        'experience_list': split_field(resume.work_experience),
        'education_list': split_field(resume.education),
        'achievements_list': split_field(resume.achievements),
    }

    html_string = render_to_string('resume/download_resume_pdf4.html', context)
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
    return response
@login_required
def resume_form5(request):
    if request.method == 'POST':
        resume = Resume5.objects.create(
            full_name=request.POST.get('full_name'),
            job_title=request.POST.get('job_title'),
            address=request.POST.get('address'),
            email=request.POST.get('email'),
            website=request.POST.get('website'),
            phone=request.POST.get('phone'),
            profile_summary=request.POST.get('profile_summary'),
            work_experience=request.POST.get('work_experience'),
            education=request.POST.get('education'),
            qualifications=request.POST.get('qualifications'),
            skills=request.POST.get('skills'),
            references=request.POST.get('references'),
            user=request.user
        )
        # ✅ Redirect to display page
        return redirect('resume_display5', resume_id=resume.id)

    return render(request, 'resume/resume_form5.html')


def resume_display5(request, resume_id):
    resume = get_object_or_404(Resume5, id=resume_id)

    def split_field(value):
        if not value:
            return []
        return [item.strip() for item in value.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    context = {
        "resume": resume,
        "profile_summary": resume.profile_summary,
        "experience_list": split_field(resume.work_experience),
        "education_list": split_field(resume.education),
        "qualifications_list": split_field(resume.qualifications),
        "skills_list": split_field(resume.skills),
        "references_list": split_field(resume.references),
    }
    return render(request, 'resume/resume_display5.html', context)

def download_resume_pdf5(request, resume_id):
    resume = get_object_or_404(Resume5, id=resume_id)
    def split_field(value):
        if not value:
            return []
        return [item.strip() for item in value.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    experience_list = split_field(resume.work_experience)
    education_list = split_field(resume.education)
    qualifications_list = split_field(resume.qualifications)
    skills_list = split_field(resume.skills)
    references_list = split_field(resume.references)

    html_string = render_to_string('resume/download_resume_pdf5.html', {
        'resume': resume,
        'profile_summary': resume.profile_summary,  # ✅ added
        'experience_list': experience_list,
        'education_list': education_list,
        'qualifications_list': qualifications_list,
        'skills_list': skills_list,
        'references_list': references_list,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response
@login_required
def my_resumes(request):
    user = request.user

    # Fetch resumes for the logged-in user from each model
    resumes1 = Resume1.objects.filter(user=user.username)
    resumes2 = Resume2.objects.filter(user=user.username)
    resumes3 = Resume3.objects.filter(user=user.username)
    resumes4 = Resume4.objects.filter(user=user.username)
    resumes5 = Resume5.objects.filter(user=user.username)

    # Organize by template for easier display
    all_resumes = {
        "Template 1": resumes1,
        "Template 2": resumes2,
        "Template 3": resumes3,
        "Template 4": resumes4,
        "Template 5": resumes5,
    }

    return render(request, 'resume/my_resumes.html', {"all_resumes": all_resumes})
@login_required
def dashboard(request):
    user = request.user
    resumes = []
    for r in Resume1.objects.filter(user=user):
        print("Found Resume1:", r.full_name)
        resumes.append({'id': r.id, 'full_name': r.full_name, 'job_title': r.job_title, 'type': 'Resume1'})
    for r in Resume2.objects.filter(user=user):
        print("Found Resume2:", r.full_name)
        resumes.append({'id': r.id, 'full_name': r.full_name, 'job_title': r.job_title, 'type': 'Resume2'})
    for r in Resume3.objects.filter(user=user):
        print("Found Resume3:", r.full_name)
        resumes.append({'id': r.id, 'full_name': r.full_name, 'job_title': r.job_title, 'type': 'Resume3'})
    for r in Resume4.objects.filter(user=user):
        print("Found Resume4:", r.full_name)
        resumes.append({'id': r.id, 'full_name': r.full_name, 'job_title': r.job_title, 'type': 'Resume4'})
    for r in Resume5.objects.filter(user=user):
        print("Found Resume5:", r.full_name)
        resumes.append({'id': r.id, 'full_name': r.full_name, 'job_title': r.job_title, 'type': 'Resume5'})

    print("✅ Total resumes found:", len(resumes))

    return render(request, 'resume/dashboard.html', {'resumes': resumes})

@login_required
def resume_display(request, resume_type, resume_id):
    model_map = {
        'Resume1': Resume1,
        'Resume2': Resume2,
        'Resume3': Resume3,
        'Resume4': Resume4,
        'Resume5': Resume5,
    }

    model = model_map.get(resume_type)
    resume = get_object_or_404(model, id=resume_id)

    def split_field(value):
        if not value:
            return []
        return [item.strip() for item in value.replace('\r', '').replace(',', '\n').splitlines() if item.strip()]

    context = {
        "resume": resume,

        # Plain text lists
        "skills_list": split_field(getattr(resume, "skills", "")),
        "languages_list": split_field(getattr(resume, "languages", "")),
        "references_list": split_field(getattr(resume, "references", "")),
        "qualifications_list": split_field(getattr(resume, "qualifications", "")),
        "projects": split_field(getattr(resume, "projects", "")),
        "achievements_list": split_field(getattr(resume, "achievements", "")),
        "experience_list": split_field(getattr(resume, "work_experience", "")),  # ✅ plain text
        "education_list": split_field(getattr(resume, "education", "")),        # ✅ plain text
        "profile_summary": getattr(resume, "profile_summary", ""),              # ✅ include summary if present
    }

    return render(request, f"resume/resume_display{resume_type[-1]}.html", context)
