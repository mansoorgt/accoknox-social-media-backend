from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Friends(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    #pending =0,accepted=1,rejected=2
    request_status=models.IntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table="friends"
    