# from django.test import TestCase
# from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
# # Create your tests here.
# from django.contrib.auth import get_user_model



# class AuthTest(APITestCase):

#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = get_user_model().objects.create_user(
#             email='user@gmail.com',
#             password= '12345',
#             is_active = True,
#             activation_code = '1234'
#         )
#     def test_register(self):
#         data= {
#             'emil': 'new_user@gmail.com',
#             'password': '123456',
#             'password_confirm': '123456',
#             'name': 'test',
#             'last_name' : 'Test'