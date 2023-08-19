from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import secrets
import pandas as pd

from client.custom_auth import TokenAuthentication
from .api_auth import APIAuthentication

from project.models import ProjectModel
from server.email import send_email, send_csv

from .models import EmailModel, EmailBoxModel, InstantReplyModel
from .validate_email import validator
from .pagination import AllEmailPagination
from .serializers import AllEmailSerializer, EmailSerializer

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle


class EmailBoxView(APIView):
    authentication_classes = [TokenAuthentication]
    pagination_class = AllEmailPagination

    # Create New EmailBox
    def post(self, request):
        user = request.user
        project_name = request.data.get("project_name")
        # Get count of projects
        count = ProjectModel.objects.filter(user=user).aggregate(project_count=Count('id'))['project_count']
        if count == 3:
            return Response({"message": "Project creation limit reached."}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Check if project name already exists
        if ProjectModel.objects.filter(name=project_name, user=user).exists():
            return Response({"message": "Project with the same name already exists."}, status=status.HTTP_409_CONFLICT)

        product = "EMAILBOX"
        key = secrets.token_hex(32)
        project = ProjectModel.objects.create(name=project_name, user=user, product=product, key=key)
        if not project:
            return Response({"message": "Failed to create project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        EmailBoxModel.objects.create(project=project)
        return Response({"message": "Project created", "project_id": project.id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        # location = request.META.get('REMOTE_ADDR', None)
        # print("location", location)
        project_id = request.GET.get("project_id")
        try:
            emailbox = EmailBoxModel.objects.get(project__id=project_id)
        except EmailBoxModel.DoesNotExist:
            return Response("EmailBox not found", status=status.HTTP_404_NOT_FOUND)

        emails = EmailModel.objects.filter(emailbox=emailbox).order_by('-time_added')

        # Apply pagination
        paginator = self.pagination_class()
        paginated_emails = paginator.paginate_queryset(emails, request)

        serializer = EmailSerializer(paginated_emails, many=True)
        response = {
            'data': serializer.data,
            'total_pages': paginator.page.paginator.num_pages
        }

        return paginator.get_paginated_response(response)


    # Read EmailBox details with its id
    # def get(self, request):
    #     project_id = request.GET["project_id"]
    #     try:
    #         emailbox = EmailBoxModel.objects.get(project__id=project_id)
    #     except:
    #         return Response("EmailBox not found", status=status.HTTP_404_NOT_FOUND)
    #     project_name = emailbox.project.name
    #     key = emailbox.project.key
    #     created_at = emailbox.project.created_at
    #     updated_at = emailbox.project.updated_at
    #     res = {
    #         "project_id": project_id,
    #         "emaibox_project_name": project_name,
    #         "emailbox_key": key,
    #         "emailbox_created_at": created_at,
    #         "emailbox_updated_at": updated_at
    #     }
    #     return Response(res, status=status.HTTP_200_OK)

    # def patch(self, request):
    #     project_id = request.data.get("project_id")
    #     print(project_id)
    #     project = ProjectModel.objects.get(id=project_id)
    #     print(request.data)
    #     if "projectName" in request.data:
    #         new_name = request.data.get("project_name")
    #         project.name = new_name
    #         project.save()
    #         print(project.name)
    #         return Response({"message": "Name Updated", "emailbox_project_name": new_name}, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         key = secrets.token_hex(32)
    #         project.key = key
    #         project.save()
    #         return Response({"message": "API Updated", "emailbox_key": key}, status=status.HTTP_202_ACCEPTED)



class EmailboxListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        emailbox = EmailBoxModel.objects.filter(project__user=user).order_by("id")
        response = []
        for eb in emailbox:
            res = {
                "name": eb.project.name,
                "project_id": eb.project.id
            }
            response.append(res)
        return Response(response, status=status.HTTP_200_OK)

class EmailboxListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        emailbox = EmailBoxModel.objects.filter(project__user=user).order_by("id")
        response = []
        for eb in emailbox:
            res = {
                "name": eb.project.name,
                "project_id": eb.project.id
            }
            response.append(res)
        return Response(response, status=status.HTTP_200_OK)

class EmailView(APIView):
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'custom_scope'
    authentication_classes = [APIAuthentication]

    def post(self, request):
        email = request.data.get("email")
        project_id = request.auth
        # print(email, project_id)
        try:
            emailbox = EmailBoxModel.objects.get(project__id=project_id)

            try:
                email_obj = EmailModel.objects.get(emailbox=emailbox, email_address=email)

                # Email already exists, update it
                email_obj.total_request += 1
                email_obj.time_added = timezone.now()
                email_obj.save()
                return Response({"message": "Email already exists."}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                # check validation of email
                # TODO: Add function in background task
                email_val = validator(email)
                # print(email_val["is_valid"])
                # Email doesn't exist, create a new one
                create = EmailModel.objects.create(emailbox=emailbox, email_address=email,
                                                   is_valid=email_val["is_valid"],
                                                   syntax_error_status=email_val["syntax_error_status"],
                                                   role_status=email_val["role_status"],
                                                   disposable_status=email_val["disposable_status"],
                                                   free_status=email_val["free_status"],
                                                   dns_status=email_val["dns_status"], role=email_val["role"],
                                                   disposable_provider=email_val["disposable_provider"],
                                                   domain=email_val["domain"], account=email_val["account"]
                                                   )
                return Response({"message": "Email Added In the EmailBox"}, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            # EmailBoxModel not found for the project
            return Response({"message": "EmailBoxModel not found"}, status=status.HTTP_404_NOT_FOUND)

class AllEmailView(APIView):
    authentication_classes = [TokenAuthentication]
    pagination_class = AllEmailPagination

    def get(self, request):
        user = request.user
        emailboxes = EmailBoxModel.objects.filter(project__user=user)
        emails = EmailModel.objects.filter(emailbox__in=emailboxes).select_related('emailbox__project').order_by(
            'time_added')
        paginator = self.pagination_class()
        paginated_emails = paginator.paginate_queryset(emails, request)

        serializer = AllEmailSerializer(paginated_emails, many=True)
        # print(serializer.data)
        return paginator.get_paginated_response(serializer.data)

class InstantView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        email_id = request.GET["emailId"]
        print(email_id)
        try:
            reply = InstantReplyModel.objects.get(email__id=email_id)
            print(reply)
            response = {
                "subject": reply.subject,
                "body": reply.body,
                "time": reply.time
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"message": "Instant Reply Available"}, status=status.HTTP_200_OK)

    def post(self, request):
        email_id = request.data.get("emailId")
        email = EmailModel.objects.get(id=email_id)
        subject = request.data.get("subject")
        body = request.data.get("body")
        send_email(email, subject, body)
        return Response({"message": "Instant Reply Sent"}, status=status.HTTP_201_CREATED)


class CSVView(APIView):

    def post(self, request):
        project_id = request.data.get("project_id")
        role_status = request.data.get("role_status")
        dns_status = request.data.get("dns_status")
        disposable_status = request.data.get("disposable_status")
        free_status = request.data.get("free_status")
        # print(EmailModel.objects.filter(emailbox__project__id=project_id))
        try:
            if free_status is True or free_status is False:
                email_objs = EmailModel.objects.filter(emailbox__project__id=project_id, role_status=role_status,
                                                       dns_status=dns_status, disposable_status=disposable_status,
                                                       free_status=free_status).values('email_address', 'is_valid',
                                                                                       'time_added', 'total_request', 'role_status', 'disposable_status', 'free_status', 'dns_status', 'role', 'disposable_provider', 'domain', 'account')
            else:
                email_objs = EmailModel.objects.filter(Q(free_status=True) | Q(free_status=False) | Q(free_status=None),
                                                       emailbox__project__id=project_id, role_status=role_status,
                                                       dns_status=dns_status,
                                                       disposable_status=disposable_status).values('email_address',
                                                                                                   'is_valid',
                                                                                                   'time_added',
                                                                                                   'total_request',  'role_status', 'disposable_status', 'free_status', 'dns_status', 'role', 'disposable_provider', 'domain', 'account')


        except ObjectDoesNotExist:
            return Response({"message": "EmailBoxModel not found"}, status=status.HTTP_404_NOT_FOUND)

        df = pd.DataFrame.from_records(email_objs, columns=['email_address', 'is_valid', 'time_added', 'total_request',  'role_status', 'disposable_status', 'free_status', 'dns_status' , 'role', 'disposable_provider', 'domain', 'account'])
        # print(df)
        csv_data = df.to_csv(index=False)
        send_csv(csv_data)

        return Response({"message": "CSV Emailed Successfully"}, status=status.HTTP_201_CREATED)



