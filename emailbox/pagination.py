from rest_framework.pagination import PageNumberPagination

class AllEmailPagination(PageNumberPagination):
    page_size = 25