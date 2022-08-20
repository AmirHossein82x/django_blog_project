from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('<int:pk>/', post_detail_view, name='posts_detail'),
    path('create/', PostCreateView.as_view(), name='post create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post delete')
]
