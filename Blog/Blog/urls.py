from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from upload.views import image_upload


urlpatterns = [

    path('upload/', image_upload, name='upload'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('image-upload', image_upload, name='image_upload'),
    path('posts/', include('posts.urls'), name='posts'),
    path('', include('pages.urls'), name='home'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
