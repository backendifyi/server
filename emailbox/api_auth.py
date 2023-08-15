from rest_framework.exceptions import AuthenticationFailed
from project.models import ProjectModel

class APIAuthentication:
    def authenticate(self, request):
        # Get the access token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Extract the token from the header
        try:
            _, token = auth_header.split()
        except ValueError:
            return None

        # Check if the token exists in the ProjectModel
        try:
            project = ProjectModel.objects.get(key=token)
        except ProjectModel.DoesNotExist:
            raise AuthenticationFailed('Invalid access token')

        # Return the authenticated project
        return (None, project.id)
