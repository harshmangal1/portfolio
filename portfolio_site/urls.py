from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect


@never_cache
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin/login/')


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


@never_cache
def admin_password_reset_request(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user or not admin_user.email:
            return render(request, 'admin/password_reset_error.html', {
                'error': 'Admin email not configured. Please contact support.'
            })
        
        if request.method == 'POST':
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(admin_user.pk))
            token = token_generator.make_token(admin_user)
            
            current_site = Site.objects.get_current()
            protocol = 'https' if request.is_secure() else 'http'
            domain = request.get_host()
            
            context = {
                'email': admin_user.email,
                'domain': domain,
                'site': current_site,
                'uid': uid,
                'token': token,
                'protocol': protocol,
            }
            
            subject = 'Portfolio Admin - Password Reset Request'
            email_template = 'admin/password_reset_email.html'
            email_message = render_to_string(email_template, context)
            
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_user.email],
                fail_silently=False,
                html_message=email_message,
            )
            
            return render(request, 'admin/password_reset_done.html')
        
        return render(request, 'admin/password_reset_request.html')
        
    except Exception as e:
        return render(request, 'admin/password_reset_error.html', {
            'error': str(e)
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-logout/', admin_logout, name='admin_logout'),
    path('dashboard/', custom_admin_index, name='custom_admin_index'),
    path('skills-management/', custom_skills_view, name='custom_skills_view'),
    path('password-reset/', admin_password_reset_request, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='admin/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='admin/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='admin/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('', include('core.urls')),
]

# Serve static files only (media is handled by Cloudinary)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
