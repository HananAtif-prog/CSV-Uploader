from django.shortcuts import render

# Create your views here.
# app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import FileUploadSerializer
from app.models import UploadedFile
from app.celery import process_uploaded_file
from celery.result import AsyncResult

class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            task = process_uploaded_file.delay(file_instance.id)
            return Response({"task_id": task.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatusView(APIView):
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        return Response({"state": task.state, "result": task.result})
