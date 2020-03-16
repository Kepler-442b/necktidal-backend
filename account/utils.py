import jwt

from .models        import User
from my_settings    import ALGORITHM, SECRET_KEY

from django.http    import HttpResponse, JsonResponse

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization', None)
            payload         = jwt.decode(access_token, SECRET_KEY['secret'], algorithms=ALGORITHM)
            user            = User.objects.get(email=payload["email"])
            request.user    = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEYS'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
