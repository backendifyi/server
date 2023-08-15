from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from client.models import AccessTokenModel

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # print("in token auth", request.headers)
        # Get the access token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Extract the token from the header
        try:
            _, token = auth_header.split()
            # print("token", token)
        except ValueError:
            return None

        # Check if the token exists in the AccessToken model
        try:
            access_token = AccessTokenModel.objects.get(token=token)
        except AccessTokenModel.DoesNotExist:
            raise AuthenticationFailed('Invalid access token')

        # Return the authenticated user and token
        print(access_token.user)
        return (access_token.user, access_token)
