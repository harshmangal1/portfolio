from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
def custom_admin_index(request):
    from portfolio.models import Project, Skill, SkillCategory, Certification
    from blog.models import BlogPost
    from contact.models import ContactMessage
    
    context = {
        'project_count': Project.objects.count(),
        'skill_count': Skill.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'certification_count': Certification.objects.count(),
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
        'recent_projects': Project.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'user': request.user,
    }
    
    skills = Skill.objects.select_related('category').all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    context['skills_by_category'] = skills_by_category
    
    return render(request, 'admin/index.html', context)


@never_cache
def custom_skills_view(request):
    from portfolio.models import Skill, SkillCategory, Project
    from blog.models import BlogPost
    from contact.models import ContactMessage
    
    skills = Skill.objects.select_related('category').all().order_by('category__order', 'order')
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    categories = SkillCategory.objects.all().order_by('order')
    
    context = {
        'project_count': Project.objects.count(),
        'skill_count': Skill.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'certification_count': 0,
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
        'recent_projects': [],
        'recent_messages': [],
        'skills_by_category': skills_by_category,
        'categories': categories,
        'user': request.user,
    }
    
    return render(request, 'admin/portfolio/skill_change_list.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin handles login/logout
    path('dashboard/', custom_admin_index, name='custom_admin_index'),
    path('skills-management/', custom_skills_view, name='custom_skills_view'),
    path('', include('core.urls')),
]

# Serve static files only (media is handled by Cloudinary)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
