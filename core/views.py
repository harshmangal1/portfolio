from django.shortcuts import render
from portfolio.models import Project, Skill, Experience, Education, Certification, SkillCategory, CurrentlyLearning
from blog.models import BlogPost
from contact.models import ContactMessage
from core.models import Profile, HeroTitle, CareerObjective, Stat
from core.github import get_github_repos


def home(request):
    profile = Profile.objects.first()
    if not profile:
        profile = Profile.objects.create(
            name="Your Name",
            title="Full Stack Developer",
            short_intro="I build beautiful web applications",
            bio="Welcome to my portfolio website."
        )
    hero_titles = HeroTitle.objects.filter(active=True)
    career_objective = CareerObjective.objects.filter(active=True).first()
    stats = Stat.objects.all().order_by('order')
    skills = Skill.objects.all().order_by('category', '-proficiency_level')
    skill_categories = SkillCategory.objects.all()
    projects = Project.objects.filter(featured=True).order_by('-created_at')[:3]
    experiences = Experience.objects.all()
    education = Education.objects.all()
    certifications = Certification.objects.all()[:4]
    blog_posts = BlogPost.objects.filter(published=True).order_by('-created_at')[:3]
    github_repos = []
    
    if profile and profile.github_username:
        github_repos = get_github_repos(profile.github_username, 6)
    
    skills_by_category = {}
    for category in skill_categories:
        category_skills = skills.filter(category=category)
        if category_skills:
            skills_by_category[category] = category_skills
    
    return render(request, 'core/home.html', {
        'profile': profile,
        'hero_titles': hero_titles,
        'career_objective': career_objective,
        'stats': stats,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'projects': projects,
        'experiences': experiences,
        'education': education,
        'certifications': certifications,
        'blog_posts': blog_posts,
        'github_repos': github_repos,
    })


def about(request):
    profile = Profile.objects.first()
    career_objective = CareerObjective.objects.filter(active=True).first()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    skill_categories = SkillCategory.objects.all()
    skills = Skill.objects.all().order_by('category', '-proficiency_level')
    currently_learning = CurrentlyLearning.objects.all().order_by('order')
    
    skills_by_category = {}
    for category in skill_categories:
        category_skills = skills.filter(category=category)
        if category_skills:
            skills_by_category[category] = category_skills
    
    return render(request, 'core/about.html', {
        'profile': profile,
        'career_objective': career_objective,
        'experiences': experiences,
        'education': education,
        'skills_by_category': skills_by_category,
        'currently_learning': currently_learning,
    })


def projects(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        projects = Project.objects.all().order_by('-featured', '-created_at')
    else:
        projects = Project.objects.filter(category=category).order_by('-featured', '-created_at')
    
    return render(request, 'core/projects.html', {
        'projects': projects,
        'current_category': category,
    })


def certifications(request):
    certifications = Certification.objects.all().order_by('-issued_date', 'order')
    return render(request, 'core/certifications.html', {
        'certifications': certifications,
    })


def certification_detail(request, credential_id):
    cert = Certification.objects.filter(credential_id=credential_id).first()
    if not cert:
        from django.shortcuts import get_object_or_404
        get_object_or_404(Certification, credential_id=credential_id)
    return render(request, 'core/certification_detail.html', {'cert': cert})


def blog_index(request):
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/index.html', {'posts': posts})


def blog_detail(request, slug):
    post = BlogPost.objects.filter(slug=slug, published=True).first()
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id).order_by('-created_at')[:3] if post else []
    return render(request, 'blog/detail.html', {'post': post, 'recent_posts': recent_posts})


def contact(request):
    profile = Profile.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        from django.contrib import messages
        messages.success(request, 'Message sent successfully!')
        return render(request, 'contact/index.html', {'profile': profile, 'sent': True})
    
    return render(request, 'contact/index.html', {'profile': profile})
