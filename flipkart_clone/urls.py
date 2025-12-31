"""
URL configuration for flipkart_clone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.defaults import page_not_found

def custom_404_redirect(request, exception=None):
    """Redirect all undefined URLs to products page"""
    return redirect('all_products', permanent=False)

def catch_all_redirect(request, path=''):
    """Catch-all redirect for undefined URLs"""
    return redirect('all_products', permanent=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('products.urls')),
]

# Handle 404 - redirect to products (works when DEBUG=False)
handler404 = custom_404_redirect

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all pattern - MUST be last (works when DEBUG=True)
urlpatterns += [
    re_path(r'^.*/$', catch_all_redirect),  # URLs ending with /
    re_path(r'^.*$', catch_all_redirect),   # All other URLs
]