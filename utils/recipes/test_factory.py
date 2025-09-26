import io
import runpy
from contextlib import redirect_stdout

from django.test import TestCase

from utils.recipes.factory import make_recipe, rand_ratio


class RecipeFactoryTest(TestCase):
    def test_rand_ratio_generates_between_840_900_w_473_573_h(self):
        width, height = rand_ratio()
        self.assertLessEqual(
            840,
            width
        )
        self.assertLessEqual(
            473,
            height
        )
        self.assertGreaterEqual(
            900,
            width
        )
        self.assertGreaterEqual(
            573,
            height
        )

    def test_make_recipe_factory_creates_fake_recipe(self):
        recipe = make_recipe()

        self.assertIsInstance(recipe['id'], int)
        self.assertIsInstance(recipe['title'], str)

    def test_factory_main_block(self):
        f = io.StringIO()
        # Capture the output of pprint
        with redirect_stdout(f):
            runpy.run_path("utils/recipes/factory.py", run_name="__main__")
        output = f.getvalue()

        # Check that expected fields are in the output
        self.assertIn("title", output)
        self.assertIn("id", output)
        self.assertIn("preparation_steps", output)
