from django.db import models


class SkillCategory(models.Model):
    name = models.CharField(max_length=50, default="Category")
    icon = models.CharField(max_length=50, default="fa-code", help_text="Font Awesome icon")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, default="Skill")
    icon = models.CharField(max_length=50, default="fa-code", help_text='Font Awesome class or emoji')
    proficiency_level = models.IntegerField(default=50, help_text='1-100')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-proficiency_level']

    def __str__(self):
        return self.name


class CurrentlyLearning(models.Model):
    name = models.CharField(max_length=100, default="Technology")
    icon = models.CharField(max_length=50, default="fa-code")
    progress = models.IntegerField(default=0, help_text="Learning progress 0-100")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('ai', 'AI / ML'),
        ('data', 'Data Analytics'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200, default="Project Title")
    short_description = models.CharField(max_length=300, default="", help_text="Short description for cards")
    description = models.TextField(default="")
    tech_stack = models.CharField(max_length=500, default="", help_text='Comma-separated technologies')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    github_link = models.URLField(max_length=200, blank=True, default="")
    live_demo = models.URLField(max_length=200, blank=True, default="")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=200, default="Certification Name")
    organization = models.CharField(max_length=200, default="Organization")
    issued_date = models.DateField()
    credential_id = models.CharField(max_length=200, blank=True, default="", help_text="Credential ID or URL")
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-issued_date', 'order']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return self.name


class Experience(models.Model):
    company = models.CharField(max_length=200, default="Company")
    position = models.CharField(max_length=200, default="Position")
    description = models.TextField(blank=True, default="")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order', '-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200, default="Institution")
    degree = models.CharField(max_length=200, default="Degree")
    field_of_study = models.CharField(max_length=200, blank=True, default="")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order', '-start_date']

    def __str__(self):
        return f"{self.degree} at {self.institution}"
