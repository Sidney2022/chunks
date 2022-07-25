import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CsvChunk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chunk_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    file = models.CharField(max_length=255)
