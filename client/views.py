import requests
import os
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .models import AccessTokenModel, ClientProfileModel

from client.custom_auth import TokenAuthentication

from google_auth_oauthlib.flow import Flow

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('AUTH_REDIRECT_URI')
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile']

client_secrets_data = json.loads(os.getenv('GOOGLE_CLIENT_SECRET_DATA'))


class GoogleAuthURLView(APIView):

    def get(self, request):
        print("called get of gauth")
        google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"

        params = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'scope': 'openid+email+profile',
            'redirect_uri': REDIRECT_URI,
        }

        auth_url = f"{google_auth_url}?client_id={params['client_id']}&response_type={params['response_type']}&scope={params['scope']}&redirect_uri={params['redirect_uri']}"
        print(auth_url)
        return Response({'auth_url': auth_url})


class GoogleAuthCallbackView(APIView):
    def post(self, request):

        code = request.data.get("code")
        # flow = Flow.from_client_secrets_file(
        #     'D:\Backendifyi\core\client\client_secret.json',
        #     scopes=SCOPES,
        #     redirect_uri=REDIRECT_URI
        # )
        flow = Flow.from_client_config(
            client_config=client_secrets_data,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
)
        flow.fetch_token(code=code, authorization_response=request.build_absolute_uri())

        credentials = flow.credentials
        access_token = credentials.token
        print(access_token)
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
        user_info = response.json()
        # Extract the required user information from the response
        # print(user_info)
        email = user_info['email']
        name = user_info['name']
        image_url = user_info['picture']
        isRegistered = User.objects.filter(email=email)
        if not isRegistered:
            user = User.objects.create_user(username=email, email=email)
            user.save()
            AccessTokenModel.objects.create(user=user, token=access_token)
            profile = ClientProfileModel.objects.create(user=user, name=name, image_url=image_url)
            profile.save()
            print("user created")
        else:
            user = isRegistered[0]
            try:
                token_obj = AccessTokenModel.objects.get(user=user)
                token_obj.token = access_token
                token_obj.save()
            except:
                AccessTokenModel.objects.create(user=user, token=access_token)

            print("token updated")

        # print(email, name)
        # print("end")

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class ProfileView(APIView):

    def get(self, request):
        user = request.user
        client_profile = ClientProfileModel.objects.get(user=user)
        res = {
            "name": client_profile.name,
            "email": user.email,
            "image_url": client_profile.image_url
        }
        print(res)
        return Response(res, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        user = request.user
        print(user)
        token_obj = AccessTokenModel.objects.get(user=user)
        token_obj.delete()
        return Response({"message": "Token Deleted"}, status=status.HTTP_200_OK)


class PageAuthView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            user = request.user
            return Response("ok", status=status.HTTP_200_OK)
        except:
            return Response("not ok")
