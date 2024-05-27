"""This is the decorator argument for generating schema from the doc string"""

import json
from functools import wraps

from ginger.http import JsonResponse

def response_validator(serializer):
    """
    This adds post processing of response based on the schema as per serializer
    This will return 500 and a list of errors
    """

    def processor(func):
        @wraps(func)
        def processing(*args, **kwargs):
            result = func(*args, **kwargs)
            result_body = json.loads(result.content.decode("utf8"))
            srl = serializer(data=result_body)
            srl.is_valid()
            if srl.errors:
                return JsonResponse(srl.errors, status=500)
            return result

        return processing

    return processor


def body_validator(serializer):
    """
    This adds pre processing of function based request handler to check the request body.
    This will return BadRequest(400) if it does not matches the defined schema
    """

    def processor(func):
        @wraps(func)
        def processing(*args, **kwargs):
            body = json.loads(args[0].body.decode("utf8"))
            srl = serializer(data=body)
            srl.is_valid()
            if srl.errors:
                return JsonResponse(srl.errors, status=400)
            result = func(*args, **kwargs)
            return result

        return processing

    return processor
