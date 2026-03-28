from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.shortcuts import render

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
    path('admin/', custom_admin_index, name='admin_index'),
    path('admin/dashboard/', custom_admin_index, name='custom_admin_index'),
    path('admin/skills/', custom_skills_view, name='custom_skills_view'),
    path('admin/other/', admin.site.urls),
    path('', include('core.urls')),
]

# Serve media files in development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
