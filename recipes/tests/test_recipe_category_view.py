from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        recipe = self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn(recipe.title, content)
        self.assertIn(
            str(recipe.preparation_time) + " " + recipe.preparation_time_unit,
            content
        )
        self.assertIn(
            str(recipe.servings) + " " + recipe.servings_unit,
            content
        )
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_dont_load_category_recipes_not_published(self): # noqa
        """Test if recipe is_published = False doesn't show """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id})
            )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))

        self.assertIs(view.func.view_class, views.RecipeListViewCategory)
