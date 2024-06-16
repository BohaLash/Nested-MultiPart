import json
from rest_framework.parsers import MultiPartParser, DataAndFiles


class NestedMultiPartParser(MultiPartParser):
    """
    Custom parser for multipart/form-data requests.
    ---
    
    On the frontend the data is being rebuild in special order
    and sent as FormData to include files along with other data 
    in JSON-like format.

    This parser is used to rebuild the data from the request.

    ---
    ### Example:
    Model has fields called `name`, `picture`, and `gallery`.
    FormData object to be parsed will look like this:
    ```
    "__data": {"name": "Some name", "picture": "__file1", "gallery": ["__file2", "__file3"]}
    "__file1": (binary)
    "__file2": (binary)
    "__file3": (binary)
    ```
    """
    def parse(self, *args, **kwargs):
        form_data: DataAndFiles = super().parse(*args, **kwargs)

        def rebuild_files(data):
            if type(data) == str and data.startswith('__file'):
                return form_data.files.get(data, None)

            if type(data) == list:
                for i, item in enumerate(data):
                    data[i] = rebuild_files(item)

            if type(data) == dict:
                for item in data:
                    data[item] = rebuild_files(data[item])

            return data

        if '__data' in form_data.data:
            data = json.loads(form_data.data['__data'])
            return rebuild_files(data)

        return form_data
