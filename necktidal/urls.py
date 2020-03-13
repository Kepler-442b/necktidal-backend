from django.urls    import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('music', include('music.urls')),
]
