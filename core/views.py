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
    hero_titles = list(HeroTitle.objects.filter(active=True))
    career_objective = CareerObjective.objects.filter(active=True).first()
    stats = list(Stat.objects.all().order_by('order'))
    skills = Skill.objects.select_related('category').all().order_by('category__order', 'order')
    skill_categories = list(SkillCategory.objects.all())
    projects = list(Project.objects.all().order_by('-created_at')[:3])
    experiences = list(Experience.objects.all())
    education = list(Education.objects.all())
    certifications = list(Certification.objects.all())
    blog_posts = list(BlogPost.objects.filter(published=True).order_by('-created_at')[:3])
    
    github_repos = []
    if profile and profile.github_username:
        github_repos = get_github_repos(profile.github_username, 6)
    
    skills_by_category = {}
    for category in skill_categories:
        category_skills = [s for s in skills if s.category_id == category.id]
        if category_skills:
            skills_by_category[category] = category_skills
    
    currently_learning = list(CurrentlyLearning.objects.all().order_by('order'))
    
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
        'currently_learning': currently_learning,
    })


def about(request):
    profile = Profile.objects.first()
    career_objective = CareerObjective.objects.filter(active=True).first()
    experiences = list(Experience.objects.all())
    education = list(Education.objects.all())
    skill_categories = list(SkillCategory.objects.all())
    skills = Skill.objects.select_related('category').all().order_by('category__order', 'order')
    currently_learning = list(CurrentlyLearning.objects.all().order_by('order'))
    
    skills_by_category = {}
    for category in skill_categories:
        category_skills = [s for s in skills if s.category_id == category.id]
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
    from django.shortcuts import get_object_or_404
    cert = get_object_or_404(Certification, credential_id=credential_id)
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
