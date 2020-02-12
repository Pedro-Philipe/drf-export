from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .renders import XLSRenderer
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
from .utils import fill_spreadsheet
import json
from faker import Faker
from random import randrange


FAKER_LANG = 'pt_BR'

def populate_users(request):
    fake = Faker(FAKER_LANG)
    users = []
    for _ in range(5000):
        users.append(
            User(
                name=fake.name(),
                job=fake.job(),
                age=randrange(100),
            )
        )
    User.objects.bulk_create(users)

    return HttpResponse(
            json.dumps({'response':'ok'}),
            content_type="application/json")



class Download(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XLSRenderer]

    def list(self, request):
        if request.accepted_renderer.format == 'xls':
            return self.xls(request)

        return super().list(self, request)

    def xls(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        output = BytesIO()

        workbook = xlsxwriter.Workbook(output)
        spreadsheet = workbook.add_worksheet("SNC")
        last_line = fill_spreadsheet(spreadsheet, queryset)

        spreadsheet.autofilter(0, 0, last_line, 3)
        workbook.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="users.xls"'

        return response
