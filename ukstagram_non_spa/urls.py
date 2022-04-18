from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import RedirectView
from django_pydenticon.views import image as pydenticon_image


urlpatterns = [
    path('admin/', admin.site.urls),
    path('identicon/image/<path:data>/', pydenticon_image, name='pydenticon_image'),
    path('accounts/', include('accounts.urls')),
    path('ukstagram/', include('ukstagram.urls')),
    path('', login_required(RedirectView.as_view(pattern_name='ukstagram:index')), name='root'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)