from django.db import models
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    name = models.CharField(max_length=100, default="Your Name")
    title = models.CharField(max_length=200, default="Full Stack Developer")
    short_intro = models.CharField(max_length=300, default="I build beautiful web applications", help_text="Short introduction for hero section")
    bio = models.TextField(default="")
    profile_image = CloudinaryField('image', blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, default="")
    linkedin = models.URLField(max_length=200, blank=True, default="")
    email = models.EmailField(max_length=200, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="", help_text="Phone number with country code")
    resume = CloudinaryField(resource_type='raw', blank=True, null=True, help_text="Upload PDF resume")
    resume_url = models.URLField(max_length=500, blank=True, default="", help_text="Direct URL to resume (e.g., Google Drive, Dropbox, or Cloudinary public URL)")
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, default="")
    meta_description = models.CharField(max_length=160, blank=True, default="")
    
    # Settings
    github_username = models.CharField(max_length=50, blank=True, default="", help_text="GitHub username for API integration")
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.name
    
    def get_resume_url(self):
        if self.resume_url:
            return self.resume_url
        if self.resume:
            return self.resume.url
        return None


class HeroTitle(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class CareerObjective(models.Model):
    title = models.CharField(max_length=200, default="Career Objective")
    content = models.TextField(default="", help_text="Your career goals and objectives")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Career Objective'
        verbose_name_plural = 'Career Objective'

    def __str__(self):
        return self.title


class Stat(models.Model):
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    value = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"
