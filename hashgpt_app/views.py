'''
Writing views
A view function, or view for short, 
is a Python function that takes a web request and returns a web response. 
This response can be the HTML contents of a web page, 
or a redirect, or a 404 error, or an XML document, or an image . . . or anything, really. 
The view itself contains whatever arbitrary logic is necessary to return that response. 
This code can live anywhere you want, as long as it’s on your Python path. 
There’s no other requirement–no “magic,” so to speak. 
For the sake of putting the code somewhere, 
the convention is to put views in a file called views.py, 
placed in your project or application directory.
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .ResponseThen import ResponseThen
from .Webhook import Webhook

@api_view(['POST'])
@permission_classes([AllowAny])
def webhook(request):
    try:
        after_response = Webhook(request.data)
        return ResponseThen(after_response.after_response, status=status.HTTP_200_OK)
    except:
        return ResponseThen(status=status.HTTP_200_OK)