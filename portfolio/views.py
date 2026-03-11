from django.shortcuts import render
from .models import Skill, Project, Experience, Education


def portfolio_index(request):
    skills = Skill.objects.all().order_by('category', '-proficiency_level')
    projects = Project.objects.all().order_by('-featured', '-created_at')
    experiences = Experience.objects.all()
    education = Education.objects.all()
    
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render(request, 'portfolio/index.html', {
        'skills_by_category': skills_by_category,
        'projects': projects,
        'experiences': experiences,
        'education': education,
    })
