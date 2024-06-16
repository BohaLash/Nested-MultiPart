import json

from rest_framework.parsers import DataAndFiles

from common.parsers import NestedMultiPartParser


class TestNestedMultiPartParser:

    def test_nested_multi_part_data(self, get_file, faker, mocker):
        data = {
            'a': 1,
            'b': 'str',
            'c': [1, 2, 3],
            'd': {
                'a': 1,
                'b': '__file1',
                'c': {'a': '__file2'},
                'd': ['__file3', '__file4'],
                'e': [
                    {'a': '__file5'},
                    {'b': '__file6'},
                ],
            },
            'f': '__file7',
        }

        files = [get_file() for _ in range(7)]

        mocker.patch(
            'common.parsers.MultiPartParser.parse',
            return_value=DataAndFiles(
                data={
                    '__data': json.dumps(data),
                },
                files={
                    '__file1': files[0],
                    '__file2': files[1],
                    '__file3': files[2],
                    '__file4': files[3],
                    '__file5': files[4],
                    '__file6': files[5],
                    '__file7': files[6],
                },
            ),
        )

        parser_class = NestedMultiPartParser()
        parsed_data = parser_class.parse(stream=b'')

        expected = {
            'a': 1,
            'b': 'str',
            'c': [1, 2, 3],
            'd': {
                'a': 1,
                'b': files[0],
                'c': {'a': files[1]},
                'd': [files[2], files[3]],
                'e': [
                    {'a': files[4]},
                    {'b': files[5]},
                ],
            },
            'f': files[6],
        }

        assert parsed_data == expected

    def test_nested_multi_part_data_no_files(self, get_file, faker, mocker):
        data = {
            'a': 1,
            'b': 'str',
            'c': [1, 2, 3],
            'd': {
                'a': 1,
                'd': ['qwerty', 'qwerty'],
                'e': [
                    {'a': 'qwerty'},
                    {'b': 'qwerty'},
                ],
            },
        }

        mocker.patch(
            'common.parsers.MultiPartParser.parse',
            return_value=DataAndFiles(
                data={
                    '__data': json.dumps(data),
                },
                files={},
            ),
        )

        parser_class = NestedMultiPartParser()
        parsed_data = parser_class.parse(stream=b'')

        expected = {
            'a': 1,
            'b': 'str',
            'c': [1, 2, 3],
            'd': {
                'a': 1,
                'd': ['qwerty', 'qwerty'],
                'e': [
                    {'a': 'qwerty'},
                    {'b': 'qwerty'},
                ],
            },
        }

        assert parsed_data == expected

    def test_nested_multi_part_data_default_format(self, get_file, faker, mocker):
        data = {
            'a': 1,
            'b': 'str',
            'c': [1, 2, 3],
            'd': {
                'a': 1,
                'd': ['qwerty', 'qwerty'],
                'e': [
                    {'a': 'qwerty'},
                    {'b': 'qwerty'},
                ],
            },
        }

        files = {
            'a': get_file(),
            'b': get_file(),
            'c': get_file(),
        }

        mocker.patch(
            'common.parsers.MultiPartParser.parse',
            return_value=DataAndFiles(
                data=data,
                files=files,
            ),
        )

        parser_class = NestedMultiPartParser()
        parsed_data = parser_class.parse(stream=b'')

        assert type(parsed_data) == DataAndFiles
        assert parsed_data.data == data
        assert parsed_data.files == files
