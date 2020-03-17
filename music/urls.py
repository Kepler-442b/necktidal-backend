from django.urls    import path
from .views         import (
    ArtistDetailView,
    ArtistTopTrackView,
    NewTrackView,
    NewAlbumView,
)

urlpatterns = [
    path('/artist/<int:artist_id>', ArtistDetailView.as_view()),
    path('/artist/<int:artist_id>/toptrack', ArtistTopTrackView.as_view()),
    path('/track/new', NewTrackView.as_view()),
    path('/album/new', NewAlbumView.as_view()),
]
