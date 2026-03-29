from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, HeroTitle, CareerObjective, Stat


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    search_fields = ('name', 'title')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'title', 'short_intro', 'bio', 'profile_image')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'email', 'phone')
        }),
        ('Files', {
            'fields': ('resume', 'resume_url')
        }),
        ('Settings', {
            'fields': ('github_username',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HeroTitle)
class HeroTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')
    list_editable = ('order', 'active')
    list_filter = ('active',)


@admin.register(CareerObjective)
class CareerObjectiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_editable = ('active',)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('icon', 'value', 'label', 'order')
    list_editable = ('value', 'label', 'order')


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = 'Portfolio Admin'
admin.site.site_title = 'Portfolio Admin Portal'
admin.site.index_title = 'Welcome to Portfolio Administration'
admin.site.index_template = 'admin/index.html'
