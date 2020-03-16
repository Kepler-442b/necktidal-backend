from django.urls    import path
from .views         import (
    ArtistDetailView,
)

urlpatterns = [
    path('/artist/<int:artist_id>', ArtistDetailView.as_view()),
]
