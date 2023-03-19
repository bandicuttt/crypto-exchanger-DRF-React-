from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context.get('view')
        status_code = renderer_context.get('response').status_code

        if 200 <= status_code < 300:
            response = {
                "messageType": 5,
                "message": {
                    "messageText": "SuccessInfo",
                    "responseBody": data,
                }
            }
        else:
            response = {
                "messageType": 6,
                "message": {
                    "messageText": "ErrorInfo",
                    "reason": self.get_error_messages(data),
                }
            }
        return super().render(response, accepted_media_type, renderer_context)

    def get_error_messages(self, data):
        if isinstance(data, (ReturnDict, dict)):
            error_messages = {}
            for key, value in data.items():
                error_messages[key] = self.get_error_messages(value)
            return error_messages
        elif isinstance(data, (ReturnList, list)):
            error_messages = []
            for item in data:
                error_messages.append(self.get_error_messages(item))
            return error_messages
        else:
            return data