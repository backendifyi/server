from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from client.custom_auth import TokenAuthentication
from .models import ProjectModel
import secrets


class APIKeyView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        project_id = request.GET["project_id"]
        # print(project_id)
        try:
            project = ProjectModel.objects.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return Response("Project not found", status=status.HTTP_404_NOT_FOUND)
        api_key = project.key
        return Response({"api_key": api_key}, status=status.HTTP_200_OK)

    def patch(self, request):
        project_id = request.data.get("project_id")
        try:
            project = ProjectModel.objects.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return Response("Project not found", status=status.HTTP_404_NOT_FOUND)
        api_key = secrets.token_hex(32)
        project.key = api_key
        project.save()
        return Response({"api_key": api_key}, status=status.HTTP_202_ACCEPTED)


class ProjectView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        project_id = request.GET.get("project_id")
        try:
            project = ProjectModel.objects.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return Response("Project not found", status=status.HTTP_404_NOT_FOUND)
        project_name = project.name
        key = project.key
        created_at = project.created_at
        updated_at = project.updated_at
        res = {
            "project_id": project_id,
            "project_name": project_name,
            "key": key,
            "created_at": created_at,
            "updated_at": updated_at
        }
        return Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        project_name = request.data.get("project_name")
        project_id = request.data.get("project_id")
        try:
            project = ProjectModel.objects.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return Response("Project not found", status=status.HTTP_404_NOT_FOUND)
        project.name = project_name
        project.save()
        return Response("Updated Project Name", status=status.HTTP_202_ACCEPTED)
