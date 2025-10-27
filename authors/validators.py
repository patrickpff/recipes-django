from collections import defaultdict

from django.core.exceptions import ValidationError

from utils.strings import is_positive_number


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self._validation_errors = defaultdict(list) \
            if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_preparation_time()
        self.clean_servings()
        data = self.data

        title = data.get('title')
        description = data.get('description')

        if title == description:
            self._validation_errors['title'].append(
                "Title cannot be equal to description"
            )
            self._validation_errors['description'].append(
                "Description cannot be equal to the title"
            )

        if self._validation_errors:
            raise self.ErrorClass(self._validation_errors)

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self._validation_errors['title'].append(
                "Title must be at least 5 characters long.")

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self._validation_errors[field_name].append(
                "Must be a positive number.")

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self._validation_errors[field_name].append(
                "Must be a positive number.")

        return field_value
