from django.db      import models
from music.models   import Artist, Album, Track

class User(models.Model):
    email                   = models.EmailField(max_length = 256)
    social_email            = models.EmailField(max_length = 256, null = True)
    password                = models.CharField(max_length = 100)
    thumbnail_url           = models.URLField(max_length = 2000, null = True)
    birthday                = models.DateField(null = True)
    first_name              = models.CharField(max_length = 100, null = True)
    last_name               = models.CharField(max_length = 100, null = True)
    gender                  = models.ForeignKey("Gender", on_delete = models.CASCADE, null = True)
    language                = models.CharField(max_length = 50, null = True)
    is_subscribed           = models.BooleanField(default = False)
    subscription            = models.ForeignKey("Subscription", on_delete = models.CASCADE, null = True)
    discount_information    = models.ForeignKey("DiscountInformation", on_delete = models.CASCADE, null = True)
    notification            = models.ManyToManyField("Notification", through = "UserNotification")
    created_at              = models.DateTimeField(auto_now_add = True)
    updated_at              = models.DateTimeField(auto_now = True, null = True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

class SocialAccount(models.Model):
    social_email    = models.CharField(max_length = 100, null = True)

    class Meta:
        db_table = 'social_accounts'

class Gender(models.Model):
    gender  = models.CharField(max_length = 50, null = True)

    class Meta:
        db_table = 'genders'

class Notification(models.Model):
    name        = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200, null = True)
    is_email    = models.BooleanField(default = False)
    is_push     = models.BooleanField(default = False)

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return self.name

class UserNotification(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    notification    = models.ForeignKey(Notification, on_delete = models.CASCADE, null = True)

class Subscription(models.Model):
    is_hifi         = models.BooleanField(default = False)
    base_price      = models.DecimalField(max_digits = 10, decimal_places = 2, default = 9.99)
    discount_plan   = models.ForeignKey("DiscountPlan", on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'subscriptions'

    def __str__(self):
        return self.name

class DiscountPlan(models.Model):
    name            = models.CharField(max_length = 100, null = True)
    description     = models.CharField(max_length = 300, null = True)
    discount_rate   = models.DecimalField(max_digits = 4, decimal_places = 2)

    class Meta:
        db_table = 'discount_plans'

    def __str__(self):
        return self.name

class DiscountInformation(models.Model):
    first_name  = models.CharField(max_length = 100)
    last_name   = models.CharField(max_length = 100)
    institution = models.CharField(max_length = 200)
    status      = models.CharField(max_length = 100, null = True)

    class Meta:
        db_table = 'discount_information'

    def __str__(self):
        return self.name

class FavoriteArtist(models.Model):
    user    = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    artist  = models.ForeignKey(Artist, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'favorite_artists'

class FavoriteAlbum(models.Model):
    user    = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    album   = models.ForeignKey(Album, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'favorite_albums'

class FavoriteTrack(models.Model):
    user    = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    track   = models.ForeignKey(Track, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'favorite_tracks'

class Playlist(models.Model):
    name        = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200, null = True)
    user        = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        db_table = 'playlists'

    def __str__(self):
        return self.name

class PlaylistTrack(models.Model):
    playlist    = models.ForeignKey(Playlist, on_delete = models.CASCADE, null = True)
    track       = models.ForeignKey(Track, on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = 'playlist_tracks'
