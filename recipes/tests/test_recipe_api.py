from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_auth_data(self, username='jondoe', password='P@ssword1!'):
        userdata = {
            'username': username,
            'password': password
        }

        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        api_url = reverse('recipes:token_obtain_pair')
        response = self.client.post(api_url, data={**userdata})

        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'Creme Brîlée',
            'description': 'Lorem ipsum dolor sit amet, '
            'consectetur adipiscing elit.',
            'preparation_time': 30,
            'preparation_time_unit': 'Minutes',
            'servings': 1,
            'servings_unit': 'Portions',
            'preparation_step': 'Fusce pulvinar lacus sed tempor efficitur. '
            'Nullam dignissim, ante ac facilisis faucibus, diam ante suscipit '
            'eros, quis interdum lectus metus eu eros. Nunc nisi nulla,'
            ' volutpat id convallis cursus, semper et mi. Vivamus quis '
            'euismod lacus. Ut in luctus elit, at efficitur libero. '
            'Vivamus viverra massa urna, a euismod nisi ultricies egestas.'
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse('recipes:recipe-api-list')
        response = self.client.get(api_url)

        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qty=wanted_number_of_recipes)

        response = self.client.get(reverse('recipes:recipe-api-list'))
        qty_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(
            wanted_number_of_recipes,
            qty_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qty=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        recipes[1]
        api_url = reverse('recipes:recipe-api-list')
        response = self.client.get(api_url)
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeApiV2Pagination.page_size', new=10)
    def test_recipe_api_list_can_load_recipes_by_category_id(self):
        category_wanted = self.make_category(name="WANTED_CATEGORY")
        category_not_wanted = self.make_category(name="NOT_WANTED_CATEGORY")
        recipes = self.make_recipe_in_batch(qty=10)

        for recipe in recipes:
            if recipe.id % 2 == 0:
                recipe.category = category_wanted
            else:
                recipe.category = category_not_wanted

            recipe.save()

        api_url = reverse('recipes:recipe-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.client.get(api_url)
        self.assertEqual(
            len(response.data.get('results')),
            5
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = reverse('recipes:recipe-api-list')
        response = self.client.post(api_url)

        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        api_url = reverse('recipes:recipe-api-list')
        auth_data = self.get_auth_data()
        response = self.client.post(
            api_url,
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {auth_data.get('jwt_access_token')}'
        )
        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arrange (config test)
        recipe = self.make_recipe()
        access_data = self.get_auth_data()
        recipe.author = access_data.get('user')
        recipe.save()

        # Action
        new_title_expected = f'Title updated by {recipe.author.username}'
        response = self.client.patch(
            reverse('recipes:recipe-api-detail', args=(recipe.id,)),
            data={
                'title': new_title_expected
            },
            HTTP_AUTHORIZATION=f'Bearer {access_data.get('jwt_access_token')}'
        )

        # Assertion
        self.assertEqual(
            response.data.get('title'),
            new_title_expected
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self): # noqa
        # Arrange (config test)
        recipe = self.make_recipe()
        owner = self.get_auth_data()
        recipe.author = owner.get('user')
        recipe.save()

        not_owner = self.get_auth_data(username='cant_update')

        # Action
        response = self.client.patch(
            reverse('recipes:recipe-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {not_owner.get('jwt_access_token')}'
        )

        self.assertEqual(
            response.status_code,
            403
        )
