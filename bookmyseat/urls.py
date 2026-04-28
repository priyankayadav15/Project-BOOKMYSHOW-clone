from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies.views import admin_dashboard

urlpatterns = [
    # ✅ MATCH THIS WITH JAZZMIN
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Apps
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),

    # Homepage
    path('', include('movies.urls')),
]

# Media + Static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)