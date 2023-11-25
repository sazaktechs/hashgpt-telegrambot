from rest_framework.response import Response

class ResponseThen(Response):
    def __init__(self, then_callback, **kwargs):
        super().__init__(**kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()