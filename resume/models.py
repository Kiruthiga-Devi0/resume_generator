from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
class Resume(models.Model):
    user= models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    job_pref = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    cgpa = models.CharField(max_length=50, blank=True)
    school_10 = models.CharField(max_length=255, blank=True)
    year_10 = models.CharField(max_length=50, blank=True)
    percentage_10 = models.CharField(max_length=50, blank=True)
    school_12 = models.CharField(max_length=255, blank=True)
    year_12 = models.CharField(max_length=50, blank=True)
    percentage_12 = models.CharField(max_length=50, blank=True)
    skills = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    certificates = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    accomplishments = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    def __str__(self):
        return self.full_name
class JobRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
class UserPreference(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    job_roles = models.ManyToManyField('JobRole', blank=True)
class Resume1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    work_experience = models.TextField(blank=True, default="")
    education = models.TextField(blank=True, default="")
    references = models.TextField(blank=True)
    template_type = models.CharField(max_length=10, default='Resume1')
    def __str__(self):
        return self.full_name
class Resume2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    about_me = models.TextField(blank=True)
    work_experience = models.TextField(blank=True, default="")
    skills = models.TextField(blank=True, help_text="Comma or line-separated")
    education = models.TextField(blank=True, help_text="One entry per line")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    template_type = models.CharField(max_length=10, default='Resume2')
    def __str__(self):
        return self.full_name
class Resume3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    languages = models.TextField(blank=True)
    references = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='resumes/', blank=True)
    template_type = models.CharField(max_length=10, default='Resume3')
    def __str__(self):
        return self.full_name
class Resume4(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_summary = models.TextField(blank=True)
    technical_skills = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    template_type = models.CharField(max_length=10, default='Resume4')
    def __str__(self):
        return self.full_name
class Resume5(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_summary = models.TextField(blank=True)
    work_experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    template_type = models.CharField(max_length=10, default='Resume5')
    def __str__(self):
        return self.full_name