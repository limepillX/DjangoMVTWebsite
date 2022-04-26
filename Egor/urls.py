from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from gosduma.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about', about_us, name='about'),
    path('mustbelogined', mustbelogined, name='mustbelogined'),
    path('social-auth/', include('social_django.urls', namespace="social")),

    path('posts/<int:post_id>', showpost, name='posts'),
    path('posts/add_new', add_post, name='addnewpost'),

    path('requests/show/<slug:typee>', show_requests, name='all_request'),
    path('request/show/<int:req_id>', show_request, name='show_request'),
    path('request/edit/<int:pk>', RequestUpdateView.as_view(), name='edit'),
    path('request/add_new', add_request, name='addnewrequest'),
    path('request/answer/<int:req_pk>', answer, name='answer'),
    path('request/answers', my_answers, name='my_answers'),

    path('login', LoginUser.as_view(), name="login"),
    path('logout', logout_user, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
