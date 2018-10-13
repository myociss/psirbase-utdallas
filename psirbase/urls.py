from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from resource.admin import psirna_admin_site


urlpatterns = [
    path('resource/', include('resource.urls')),
    path('admin/', psirna_admin_site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)