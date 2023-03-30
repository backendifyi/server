from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class NewsEmailView(APIView):

    def post(self, request):
        email = request.data.get("email")
        return Response(email, status=status.HTTP_201_CREATED)
