from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpage/', include('adminpage.urls', namespace='adminpage')),
    path('user/', include('authy.urls', namespace='user')),
    path('cinema/', include('cinema.urls', namespace='cinema')),
    path('celery-progress/', include('celery_progress.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
