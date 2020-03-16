import json

from .models        import (
    Artist,
    Track,
    Album,
    ArtistTrack,
    ArtistAlbum,
    AlbumTrack
)

from django.test    import TestCase
from django.test    import Client

class ArtistTest(TestCase):

    def setUp(self):
        client = Client()
        Artist.objects.create(
            id = 1,
            name = 'Future',
            thumbnail_url = 'https://resources.tidal.com/images/8faf1ca1/6130/45da/9d10/6d9f4b825605/480x480.jpg',
        )

    def test_artist_get_success(self):
        client = Client()
        response = client.get('/music/artist/1')
        self.assertEqual(response.json(),
            {
               'artist':{
                    'id'            : 1,
                    'name'          : 'Future',
                    'thumbnail_url' : 'https://resources.tidal.com/images/8faf1ca1/6130/45da/9d10/6d9f4b825605/480x480.jpg',
                    'description'   : None,
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_get_fail(self):
        client = Client()
        response = client.get('/music/artist/20000')
        self.assertEqual(response.json(),
            {
               'message':'NO_ARTIST'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_artist_get_not_found(self):
        client = Client()
        response = client.get('/music/aritst?artist_id=84')
        self.assertEqual(response.status_code, 404)

class ArtistTopTrackTest(TestCase):

    def setUp(self):
        client = Client()
        Artist.objects.create(
            id   = 1,
            name = 'Future',
        )
        Track.objects.create(
            id          = 1,
            name        = 'Baby Pluto',
            time        = '00:03:30.000000',
            music_url   = None,
            is_master   = 0,
            is_explicit = 0,
        )

        ArtistTrack.objects.create(artist_id = 1, track_id = 1)

        Album.objects.create(
            id = 1,
            name = 'Eternal Atake',
            thumbnail_url = 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg'
        )

        AlbumTrack.objects.create(album_id = 1, track_id = 1)

    def test_artist_toptrack_get_success(self):
        client = Client()
        response = client.get('/music/artist/1/toptrack')
        self.assertEqual(response.json(),
            {
                'tracks':[{
                    'id'            : 1,
                    'name'          : 'Baby Pluto',
                    'time'          : '00:03:30',
                    'music_url'     : None,
                    'is_master'     : False,
                    'is_explicit'   : False,
                    'artist_info'   : [{
                        'id'    : 1,
                        'name'  : 'Future'
                    }],
                    'album_info'    : [{
                        'id'            : 1,
                        'name'          : 'Eternal Atake',
                        'thumbnail_url' : 'https://resources.tidal.com/images/cd542e79/dce0/4809/9f3e/1c3cb2203436/320x320.jpg',
                        }
                    ]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_artist_toptrack_get_fail(self):
        client = Client()
        response = client.get('/music/artist/2/toptrack')
        self.assertEqual(response.json(),
            {
               'message':'NO_TRACK'
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_artist_toptrack_get_not_found(self):
        client = Client()
        response = client.get('/music/aritst/toptrack?artist_id=84')
        self.assertEqual(response.status_code, 404)
