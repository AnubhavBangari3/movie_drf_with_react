from django.urls import path,include
from .views import *

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('users',UserViewset,basename="users")
router.register('movies',MovieViewset,basename="movies")

urlpatterns = [
  path('',include(router.urls)),
  path('logout',LogoutView.as_view(),name="logout"),
  path('currentUser/',getCurrentUser.as_view(),name="currentUser"),
  path('movies/<int:pk>/like',likeMovie.as_view(),name="like_movie"),
  path('movies/<int:pk>/dislike',dislikeMovie.as_view(),name="dislike_movie"),
  path('Personalized',PersonalizedView.as_view(),name="Personalized"),
  path("recommend",ReommendView.as_view(),name="recommend")
]