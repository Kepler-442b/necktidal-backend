import json
import re
import bcrypt
import jwt

from django.views           import View
from django.http            import HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from my_settings            import SECRET_KEY, ALGORITHM
from .models                import User

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})"

class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            validate_email(data['email'])

            if not re.match(PASSWORD_REGEX, data['password']):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status = 400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "USER_EXISTS"}, status = 400)

            password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User(
                email       = data['email'],
                password   = password,
            ).save()

            return HttpResponse(status = 200)

        except ValidationError:
            return JsonResponse({"message": "INVALID_FORMAT"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'email': user.email}, SECRET_KEY['secret'], algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse({"Authorization": token}, status = 200)

            return HttpResponse(status = 401)

        except User.DoesNotExist:
            return HttpResponse(status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
