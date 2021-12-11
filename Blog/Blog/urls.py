from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap


from posts.sitemaps import PostSitemap
from upload.views import image_upload

sitemaps = {
    'post': PostSitemap,
}

urlpatterns = [

    path('upload/', image_upload, name='upload'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('image-upload', image_upload, name='image_upload'),
    path('posts/', include('posts.urls'), name='posts'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path('', include('pages.urls'), name='pages'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
