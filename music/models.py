from django.db      import models

class Artist(models.Model):
    name            = models.CharField(max_length = 200)
    thumbnail_url   = models.URLField(max_length = 2000, null = True)
    description     = models.TextField(null = True)
    gender          = models.ForeignKey('account.Gender', on_delete = models.SET_NULL, null = True)
    album           = models.ManyToManyField('Album', through = 'ArtistAlbum')
    track           = models.ManyToManyField('Track', through = 'ArtistTrack')
    social_media    = models.ManyToManyField('SocialMedia', through = 'ArtistSocialMedia')

    class Meta:
        db_table = 'artists'

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    name        = models.CharField(max_length = 50, null = True)
    icon_url    = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'social_media'

class ArtistSocialMedia(models.Model):
    artist          = models.ForeignKey(Artist, on_delete = models.CASCADE, null = True)
    social_media    = models.ForeignKey(SocialMedia, on_delete = models.CASCADE, null = True)
    account_url     = models.URLField(max_length = 2000, null = True)

    class Meta:
        db_table = 'artist_social_media'

class Album(models.Model):
    name            = models.CharField(max_length = 200)
    thumbnail_url   = models.URLField(max_length = 2000, null = True)
    released_date   = models.DateTimeField(null = True)
    is_live         = models.BooleanField(null = True)
    is_single       = models.BooleanField(null = True)
    track           = models.ManyToManyField('Track', through = 'AlbumTrack')
    genre           = models.ManyToManyField('Genre', through = 'AlbumGenre')

    class Meta:
        db_table = 'albums'

    def __str__(self):
        return self.name

class Genre(models.Model):
    name    = models.CharField(max_length = 50)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name

class AlbumGenre(models.Model):
    album   = models.ForeignKey(Album, on_delete = models.CASCADE)
    genre   = models.ForeignKey(Genre, on_delete = models.CASCADE)

    class Meta:
        db_table = 'album_genres'

class Track(models.Model):
    name            = models.CharField(max_length = 200)
    music_url       = models.URLField(max_length = 2000, null = True)
    time            = models.TimeField()
    is_explicit     = models.BooleanField(null = True)
    is_master       = models.BooleanField(null = True)
    credit          = models.TextField(null = True)

    class Meta:
        db_table = 'tracks'

    def __str__(self):
        return self.name

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
