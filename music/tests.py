import json

from .models        import (
    Artist
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
