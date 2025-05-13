from django.contrib import admin
from django.urls import path
from Snap_Gram import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('accounts/login/', views.login_view, name='login'),  
    path('accounts/register/', views.register_view, name='register'),
    path('upload/', views.upload_post, name='upload_post'), 
    path('feed/', views.feed, name='feed'),
    path('upload/', views.upload_photo, name='upload'), 
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('logout/', views.logout_view, name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
