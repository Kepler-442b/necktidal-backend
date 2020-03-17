from django.urls import path
from .views      import UserCheckView, SignUpView, SignInView, SocialSignInView, CollectionView

urlpatterns = [
    path('/', UserCheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/collection', CollectionView.as_view()),
    path('/social_signin', SocialSignInView.as_view()),
]
