from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import EmailModel
from .serializers import EmailSerializer

class NewsEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            # print(serializer)
            if EmailModel.objects.filter(email=email).exists():
                return Response({'email': 'Email already exists.'}, status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
