from random import uniform, choice, choices

import pytest
from unittest.mock import MagicMock
from factory import Faker
from ddf import G, N, F, M, C, teach

from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def faker():
    def evaluate(provider):
        return Faker(provider).evaluate(
            {}, None, {'locale': Faker._DEFAULT_LOCALE})
    return evaluate


@pytest.fixture
def get_file(faker):
    def file():
        extension, content_type = choice([
            ('png', 'image/png'),
            ('jpg', 'image/jpeg'),
            ('mp4', 'video/mp4'),
            ('pdf', 'application/pdf'),
        ])
        name = f"{faker('word')}.{extension}"
        file = SimpleUploadedFile(
            name, str.encode(faker('text')), content_type=content_type)
        return file
    return file
