from django.urls import include, path, re_path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='post')
router.register(r'co-admins', CoAdminsViewSet, basename='co-admin'),


urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('register/', CreateUserView.as_view(), name='register'),
    path('add-admin/', AddAdmin.as_view(), name='add-admin'),
    path('login/', Login.as_view(), name='api_token_auth'),  # <-- And here
    path('update-coadmin/<int:pk>',UpdateCoAdmin.as_view(),name='update-coadmin'),
    path('students/<int:pk>/', StudentDetail.as_view()),
    
    path('add-post/', AddPostView.as_view(), name='add'),
    path('post/<int:pk>', SinglePostView.as_view()),
    
    path('api-auth/', include('rest_framework.urls')),
]