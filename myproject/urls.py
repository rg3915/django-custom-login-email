from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('myproject.core.urls', namespace='core')),
    path('accounts/', include('myproject.accounts.urls')),  # without namespace
    path('admin/', admin.site.urls),
]
