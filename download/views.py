from django.shortcuts import render
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .renders import XLSRenderer, PDFRenderer
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
from .utils import fill_spreadsheet, DataToPdf
import json
from faker import Faker
from random import randrange
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from weasyprint import HTML


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

import os, time, datetime
from django.forms.models import model_to_dict


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

    renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
        XLSRenderer,
        PDFRenderer
    ]

    def list(self, request):
        if request.accepted_renderer.format == 'xls':
            return self.xls(request)

        if request.accepted_renderer.format == 'pdf':
            return self.pdf_teste(request)

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

        return FileResponse(output, as_attachment=True, filename='users.xls')

    def pdf(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        fields = (
            ('name', 'Name'),
            ('job', 'Job'),
            ('age', 'Age'),
        )

        doc = DataToPdf(fields, queryset, title='Título')
        doc.export('/tmp/users.pdf')

        fs = FileSystemStorage("/tmp")
        with fs.open("users.pdf") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="users.pdf"'
            return response

        return response

    def pdf_teste(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        html_string = render_to_string('pdf_template.html', {'users': queryset})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/users.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open('users.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="users.pdf"'
            return response

        return response