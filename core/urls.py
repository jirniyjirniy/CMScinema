from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpage/', include('adminpage.urls', namespace='adminpage')),
    path('user/', include('authy.urls', namespace='user')),
    path('cinema/', include('cinema.urls', namespace='cinema')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)