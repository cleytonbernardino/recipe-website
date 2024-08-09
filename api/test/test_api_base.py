from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class ApiTestMixin(test.APITestCase, RecipeMixin):
    def get_response_list(self, parameters: str = ''):
        url = reverse('api:recipe-api-list') + parameters
        return self.client.get(url)

    def get_response_detail(self, pk: int):
        url = reverse('api:recipe-api-detail', kwargs={
            'pk': pk
        })
        return self.client.get(url)

    def get_author_access_data(self, username="User_test", password="123") -> dict:
        """
        Create a new user and return it with its jwt tokens

        Args:
            username (str, optional): name of the user to be created. Defaults to "User_test".
            password (str, optional): user password. Defaults to "123".

        Returns:
            dict: dictionary containing:
            author - user data.
            access - access token.
            refresh - refresh token.
        """
        token_url = reverse('api:token_obtain_pair')
        author = self.make_author(
            username=username,
            password=password
        )
        response = self.client.post(
            token_url,
            data={
                "username": username,
                "password": password,
            }
        )
        return {'author': author, **response.data}
