import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
User = get_user_model()



class CsvChunk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    upload_time = models.DateTimeField(default=timezone.now,blank=True,)
    file = models.FileField(upload_to='files')
    
    class Meta:
        ordering = ("-user", "upload_time")
    

    @property
    def delete_after_five_minutes(self):
        time = self.upload_time+ datetime.timedelta(minutes=2)
        if time < datetime.datetime.now():
            e = CsvChunk.objects.get(file_id=self.file_id)
            e.delete()
            return True
        else:
            return False
  
  

# class CsvChunkManager(models.Manager):
    
#     def get_queryset(self):
#         return super().get_queryset().filter(
#             upload_time__gte=timezone.now()-timezone.timedelta(minutes=2)
#         )
        

# CsvChunk._base_manager.filter(
#     upload_time__lt=timezone.now()-timezone.timedelta(minutes=2)
# ).delete()

