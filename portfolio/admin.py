from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from adminsortable2.admin import SortableAdminMixin
from .models import SkillCategory, Skill, CurrentlyLearning, Project, Certification, Experience, Education


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    list_editable = ('icon', 'order')
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('skills/', staff_member_required(self.admin_site.admin_view(self.skills_view)), name='portfolio_skills_view'),
        ]
        return custom_urls + urls
    
    def skills_view(self, request):
        skills = Skill.objects.select_related('category').all().order_by('category__order', 'order')
        skills_by_category = {}
        for skill in skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        categories = SkillCategory.objects.all().order_by('order')
        context = {
            **self.admin_site.each_context(request),
            'skills_by_category': skills_by_category,
            'categories': categories,
            'title': 'Skills Management',
        }
        return render(request, 'admin/portfolio/skill_change_list.html', context)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_level', 'order')
    list_filter = ('category',)
    search_fields = ('name', 'usage_description')
    list_editable = ('proficiency_level', 'order')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'icon', 'category', 'order')
        }),
        ('Proficiency', {
            'fields': ('proficiency_level', 'usage_description')
        }),
    )


@admin.register(CurrentlyLearning)
class CurrentlyLearningAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress', 'order')
    list_editable = ('progress', 'order')


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'order', 'category', 'featured', 'created_at')
    list_filter = ('featured', 'category')
    search_fields = ('title', 'tech_stack', 'problem_statement', 'solution', 'outcome')
    readonly_fields = ('created_at',)
    list_editable = ('order', 'featured', 'category')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'short_description', 'description', 'category', 'featured', 'order', 'image')
        }),
        ('Project Details', {
            'fields': ('problem_statement', 'solution', 'outcome', 'tech_stack')
        }),
        ('Links', {
            'fields': ('github_link', 'live_demo')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'issued_date', 'order')
    search_fields = ('name', 'organization')
    list_editable = ('order',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'organization', 'issued_date', 'order')
        }),
        ('Media', {
            'fields': ('image', 'document')
        }),
        ('Credential', {
            'fields': ('credential_id',)
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date', 'current')
    list_filter = ('current',)
    search_fields = ('position', 'company')
    list_editable = ('current',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_date', 'end_date', 'current')
    list_filter = ('current',)
    search_fields = ('degree', 'institution')
    list_editable = ('current',)
