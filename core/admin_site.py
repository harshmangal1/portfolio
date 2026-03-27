from django.contrib.admin import AdminSite


class PortfolioAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        from portfolio.models import Project, Skill, SkillCategory, Certification
        from blog.models import BlogPost
        from contact.models import ContactMessage
        
        extra_context = extra_context or {}
        extra_context['project_count'] = Project.objects.count()
        extra_context['skill_count'] = Skill.objects.count()
        extra_context['blog_count'] = BlogPost.objects.count()
        extra_context['certification_count'] = Certification.objects.count()
        extra_context['unread_messages'] = ContactMessage.objects.filter(read=False).count()
        extra_context['recent_projects'] = Project.objects.order_by('-created_at')[:5]
        extra_context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        
        skills = Skill.objects.select_related('category').all()
        skills_by_category = {}
        for skill in skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        extra_context['skills_by_category'] = skills_by_category
        
        return super().index(request, extra_context)


portfolio_admin_site = PortfolioAdminSite(name='portfolio_admin')
