import openai
import re
class ExceptionHandler:
    def response(self, test):
                try:
                    response = test()
                    return response
                except openai.APIConnectionError as e:
                    reply = ("""
APIConnectionError                   
Cause: Issue connecting to openai services.
Solution: Check your network settings, proxy configuration, SSL certificates, or firewall rules.
                                """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.APITimeoutError as e:
                    reply = ("""
APITimeoutError
Cause: Request timed out.
Solution: Retry your request after a brief wait and contact openai if the issue persists.
                                """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.AuthenticationError as e:
                    reply = ("""
AuthenticationError
Cause: Your API key or token was invalid, expired, or revoked.
Solution: Check your API key or token and make sure it is correct and active. You may need to generate a new one from your account dashboard.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.BadRequestError as e:
                    reply = ("""
BadRequestError
Cause: Your request was malformed or missing some required parameters, such as a token or an input.
Solution: The error message should advise you on the specific error made. Check the documentation for the specific API method you are calling and make sure you are sending valid and complete parameters. You may also need to check the encoding, format, or size of your request data.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.ConflictError as e:
                    reply = ("""
ConflictError
Cause: The resource was updated by another request.
Solution: Try to update the resource again and ensure no other requests are trying to update it.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.InternalServerError as e:
                    reply = ("""
InternalServerError
Cause: Issue on openai side.
Solution: Retry your request after a brief wait and contact openai if the issue persists.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.NotFoundError as e:
                    reply = ("""
NotFoundError
Cause: Requested resource does not exist.
Solution: Ensure you are the correct resource identifier.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.PermissionDeniedError as e:
                    reply = ("""
PermissionDeniedError
Cause: You don't have access to the requested resource.
Solution: Ensure you are using the correct API key, organization ID, and resource ID.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.RateLimitError as e:
                    reply = ("""
RateLimitError
Cause: You have hit your assigned rate limit.
Solution: Pace your requests. Read more in openai Rate limit guide https://platform.openai.com/docs/guides/rate-limits
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except openai.UnprocessableEntityError as e:
                    reply = ("""
UnprocessableEntityError
Cause: Unable to process the request despite the format being correct.
Solution: Please try the request again.
                                 """)
                    result = re.search(r'{\'message\':(.*?).\',', str(e))
                    if result:
                        reply = result.group(1).strip()
                        reply = reply[1:]
                    return reply
                except Exception as e:
                    reply = "Error!"
                    return reply
