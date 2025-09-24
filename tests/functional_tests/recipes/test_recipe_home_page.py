import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_no_recipes_published_message(self): # noqa
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertIn('There are no recipes published yet.', body.text)
