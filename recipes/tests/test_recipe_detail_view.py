from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):        
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))

        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detailed page'
        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)
        self.assertIn(
            str(recipe.preparation_time) + " " + recipe.preparation_time_unit,
            content
        )
        self.assertIn(
            str(recipe.servings) + " " + recipe.servings_unit,
            content
        )

    def test_recipe_detail_template_dont_load_category_recipes_not_published(self): # noqa
        """Test if recipe is_published = False doesn't show """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )

        self.assertEqual(response.status_code, 404)