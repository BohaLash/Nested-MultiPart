# Nested-MultiPart
 TS and Python DRF implementation for nested multipart objects (de)serialization


### Use in DRF project:
  Edit `settings.py`:
  ```py
REST_FRAMEWORK = {
    # ...,
    'DEFAULT_PARSER_CLASSES': [
        # ...,
        'crm.parsers.NestedMultiPartParser',
    ],
}
  ```
