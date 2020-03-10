from django.db import models

class Artist(models.Model):
    name            = models.CharField(max_length = 200)
    thumbnail_url   = models.URLField(max_length = 2000, null = True)
    facebook        = models.URLField(max_length = 2000, null = True)
    twitter         = models.URLField(max_length = 2000, null = True)
    description     = models.TextField(null = True)
    album           = models.ManyToManyField('Album', through = 'ArtistAlbum')
    track           = models.ManyToManyField('Track', through = 'ArtistTrack')
    related_artist  = models.ManyToManyField('self', through = 'RelatedArtist', symmetrical = False)

    class Meta:
        db_table = 'artists'

    def __str__(self):
        return self.name

class RelatedArtist(models.Model):
    from_artists    = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True, related_name = 'from_artists')
    to_artists      = models.ForeignKey(Artist, on_delete = models.SET_NULL, null = True, related_name = 'to_artists')

    class Meta:
        unique_together = ('from_artists', 'to_artists')
        db_table        = 'related_artists'

class Album(models.Model):
    name            = models.CharField(max_length = 200)
    thumbnail_url   = models.URLField(max_length = 2000, null = True)
    released_date   = models.DateTimeField(null = True)
    is_live         = models.BooleanField(null = True)
    is_single       = models.BooleanField(null = True)
    track           = models.ManyToManyField('Track', through = 'AlbumTrack')
    related_albums  = models.ManyToManyField('self', through = 'RelatedAlbum', symmetrical = False)

    class Meta:
        db_table = 'albums'

    def __str__(self):
        return self.name

class RelatedAlbum(models.Model):
    from_albums = models.ForeignKey(Album, on_delete = models.SET_NULL, null = True, related_name = 'from_albums')
    to_albums   = models.ForeignKey(Album, on_delete = models.SET_NULL, null = True, related_name = 'to_albums')

    class Meta:
        unique_together = ('from_albums', 'to_albums')
        db_table        = 'related_albums'

class Track(models.Model):
    name            = models.CharField(max_length = 200)
    time            = models.CharField(max_length = 50)
    is_explicit     = models.BooleanField(null = True)
    is_master       = models.BooleanField(null = True)
    credit          = models.TextField(null = True)
    related_track   = models.ManyToManyField('self', through = 'RelatedTrack', symmetrical = False)

    class Meta:
        db_table = 'tracks'

    def __str__(self):
        return self.name

class RelatedTrack(models.Model):
    from_tracks = models.ForeignKey(Track, on_delete = models.SET_NULL, null = True, related_name = 'from_tracks')
    to_tracks   = models.ForeignKey(Track, on_delete = models.SET_NULL, null = True, related_name = 'to_tracks')

    class Meta:
        unique_together = ('from_tracks', 'to_tracks')
        db_table        = 'related_tracks'

class ArtistAlbum(models.Model):
    artist   = models.ForeignKey(Artist, on_delete = models.CASCADE, null = True)
    album    = models.ForeignKey(Album, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'artist_albums'

class ArtistTrack(models.Model):
    artist   = models.ForeignKey(Artist, on_delete = models.CASCADE, null = True)
    track    = models.ForeignKey(Track, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'artist_tracks'

class AlbumTrack(models.Model):
    album    = models.ForeignKey(Album, on_delete = models.CASCADE, null = True)
    track    = models.ForeignKey(Track, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'album_tracks'

