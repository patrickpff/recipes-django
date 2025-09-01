from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'There are no recipes published yet.',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published = False doesn't show """
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'There are no recipes published yet.',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_template_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn(recipe.title, content)
        self.assertIn(str(recipe.preparation_time) + " " + recipe.preparation_time_unit, content)
        self.assertIn(str(recipe.servings) + " " + recipe.servings_unit, content)
        self.assertEqual(len(response_context_recipes), 1)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_template_is_paginated(self):
        for i in range(9):
            kwargs = {
                'slug': f'r{i}',
                'author_data': {
                    'username': f'u{i}'
                }
            }

            self.make_recipe(**kwargs)
        
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
    
    def test_recipe_home_template_is_paginated_page_incomplete(self):
        for i in range(9):
            kwargs = {
                'slug': f'r{i}',
                'author_data': {
                    'username': f'u{i}'
                }
            }

            self.make_recipe(**kwargs)
        
        with patch('recipes.views.PER_PAGE', new=6):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator
            
            self.assertEqual(paginator.num_pages, 2)
            self.assertEqual(len(paginator.get_page(1)), 6)
            self.assertEqual(len(paginator.get_page(2)), 3)