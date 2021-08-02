from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views


app_name = 'boards'
urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('create/', views.board_create, name='board_create'),
    path('<int:pk>/update/', views.board_update, name='board_update'),
    path('<int:pk>/delete/', views.board_delete, name='board_delete'),
    path('<int:pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('<int:pk>/new/', views.new_topic, name='new_topic'),
    path('<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('<int:pk>/topics/<int:topic_pk>/reply', views.reply_topic, name='reply_topic'),
    path('<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/topics/<int:topic_pk>/to_csv/', views.export_topic_csv, name="to_csv"),
    path('<int:pk>/topics/<int:topic_pk>/to_pdf/', views.export_topic_pdf, name="to_pdf"),
    path('<int:pk>/topics/<int:topic_pk>/gallery/', views.gallery_images, name="gallery_images"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)