from django.urls    import path
from .views         import (
    ArtistDetailView,
    ArtistTopTrackView,
)

urlpatterns = [
    path('/artist/<int:artist_id>', ArtistDetailView.as_view()),
    path('/artist/<int:artist_id>/toptrack', ArtistTopTrackView.as_view()),
]
