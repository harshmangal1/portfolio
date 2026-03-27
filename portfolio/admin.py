from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import SkillCategory, Skill, CurrentlyLearning, Project, Certification, Experience, Education


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    list_editable = ('icon', 'order')


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
    search_fields = ('title', 'tech_stack')
    readonly_fields = ('created_at',)
    list_editable = ('order', 'featured', 'category')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'issued_date', 'order')
    search_fields = ('name', 'organization')
    list_editable = ('order',)


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
