from django.urls import path
from django.http import HttpResponse
from . import views

def reset_admin_password(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user, created = User.objects.get_or_create(username='admin')
    user.set_password('Admin@123')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return HttpResponse(f"Admin password reset! Username: admin, Password: Admin@123<br><a href='/admin/'>Go to Admin</a>")

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('certifications/', views.certifications, name='certifications'),
    path('certifications/<str:credential_id>/', views.certification_detail, name='certification_detail'),
    path('blog/', views.blog_index, name='blog_index'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('reset-admin/', reset_admin_password),
]
