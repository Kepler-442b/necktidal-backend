import json

from .models    import (
    Artist
)

from django.views   import View
from django.http    import HttpResponse, JsonResponse

class ArtistDetailView(View):
    def get(self, request, artist_id):

        if Artist.objects.filter(id = artist_id).exists():
            artist              = Artist.objects.get(id = artist_id)
            artist_attribute    = {
                'id'            : artist.id,
                'name'          : artist.name,
                'thumbnail_url' : artist.thumbnail_url,
                'description'   : artist.description,
            }

            return JsonResponse({'artist':artist_attribute}, status = 200)

        return JsonResponse({'message':'NO_ARTIST'}, status = 400)
