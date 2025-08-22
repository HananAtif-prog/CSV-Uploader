import csv
from celery import shared_task
from app.models import UploadedFile


@shared_task
def process_uploaded_file(file_id):
    file_obj = UploadedFile.objects.get(id=file_id)
    file_path = file_obj.file.path

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
    
    return f"File {file_obj.id} processed successfully!"
