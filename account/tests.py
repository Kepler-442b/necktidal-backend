from django.test import TestCase

import  json
import  bcrypt

from django.test    import TestCase
from django.test    import Client

from .models        import User

class UserTest(TestCase):
    def setUp(self):
        check = '12Ab34Cd!!'
        User.objects.create(
            email       = 'skim1025@abc.abc',
            password    = bcrypt.hashpw(check.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_view_post_success(self):
        user    = {
            'email'     : 'skim1026@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response    = Client().post('/account', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_view_post_invalid_password(self):
        user    = {
            'email'     : 'skim1026@abc.abc',
            'password'  : '12345'
        }
        response = Client().post('/account', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_PASSWORD"
            }
        )

    def test_signup_view_post_existing_user(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "USER_EXISTS"
            }
        )

    def test_signup_view_post_invalid_format(self):
        user    = {
            'email'     : '.@.',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_FORMAT"
            }
        )

    def test_signup_view_post_invalid_keys(self):
        user    = {
            'name'      : 'skim1026@abc.abc',
            'password'  : '12Ab34Cd!!'
        }
        response = Client().post('/account', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_KEYS"
            }
        )

    def test_signin_view_post_success(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response    = Client().post('/account/signin', json.dumps(user), content_type='applications/json')
        token       = response.json()['Authorization']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                "Authorization": token
            }
        )

    def test_signin_view_post_incorrect_password(self):
        user    = {
            'email'     : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 401)

    def test_signin_view_post_invalid_user(self):
        user    = {
            'email'     : 'skim1027@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)

    def test_signin_view_post_key_error(self):
        user    = {
            'name'      : 'skim1025@abc.abc',
            'password'  : '12Ab34Cd!!',
        }
        response = Client().post('/account/signin', json.dumps(user), content_type='applications/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "message": "INVALID_KEYS"
            }
        )
