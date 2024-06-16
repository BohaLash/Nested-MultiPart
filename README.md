# Nested-MultiPart
 TS and Python DRF implementation for nested multipart objects (de)serialization


### Use in DRF project:
  1. Add code from `parsers.py` to your project.
  2. Edit `settings.py`:
  ```py
REST_FRAMEWORK = {
    # ...,
    'DEFAULT_PARSER_CLASSES': [
        # ...,
        'common.parsers.NestedMultiPartParser',
    ],
}
```

### Use in TS project:
  1. Add code from `serializers.ts` to your project.
  2. Use like this:
```ts
import { buildNestedFormDataWithFiles } from '@/utils/serializers'
const payload = buildNestedFormDataWithFiles(object)
```
