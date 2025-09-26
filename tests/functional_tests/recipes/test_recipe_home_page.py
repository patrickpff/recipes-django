from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_no_recipes_published_message(self): # noqa
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertIn('There are no recipes published yet.', body.text)

    def test_recipe_home_page_with_recipes_no_recipes_published_message_dont_show(self): # noqa
        self.make_recipe()
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertNotIn('There are no recipes published yet.', body.text)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipes(self): # noqa
        recipes = self.make_recipe_in_batch()

        # User opens the page
        self.browser.get(self.live_server_url)

        # User sees the search field with the
        # placeholder "Search for a recipe..."
        search_input = self.browser.find_element(
            by=By.XPATH,
            value='//input[@placeholder="Search for a recipe..."]'
        )

        # Click at the input and type in the search term
        # "Recipe title 1" to find a recipe with this title
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        # Wait until the main content list contains the recipe title
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "recipe-list-item")
            )
        )

        # User finds what he needed
        self.assertIn(
            recipes[0].title,
            self.browser.find_element(
                by=By.CLASS_NAME, value='main-content-list'
            ).text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self): # noqa
        self.make_recipe_in_batch()

        # User opens the page
        self.browser.get(self.live_server_url)

        # Check for pagination and click on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Check if there is two more recipes on page 2
        self.assertEqual(
            len(self.browser.find_elements(by=By.CLASS_NAME, value='recipe')),
            2
        )
