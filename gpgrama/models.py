from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.forms.fields import FileField, ImageField
from fernet_fields import EncryptedCharField
import uuid

#para login
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="") #relacao 1-1 com User da tabela auth_user para fazer login
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = EncryptedCharField(max_length=200, null=False, blank=False, default="")
    email = models.EmailField(unique=True, null=False, blank=True, default="")
    password  = EncryptedCharField(max_length=50, null=False, blank=False, default="")
    type = models.IntegerField(null=False, blank=False, default=0)
    image = models.ImageField(upload_to="images/admin", blank=True)

class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="") #relacao 1-1 com User da tabela auth_user para fazer login
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = EncryptedCharField(max_length=200, null=False, blank=False, default="")
    email = models.EmailField(unique=True, null=False, blank=True, default="")
    password  = EncryptedCharField(max_length=50, null=False, blank=False, default="")
    type = models.IntegerField(null=False, blank=False, default=1)
    image = models.ImageField(upload_to="images/hr", blank=True)

    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def classname(obj):
        return obj.__class__.__name__

class HiringManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="") #relacao 1-1 com User da tabela auth_user para fazer login
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    #id = models.IntegerField(null=False, blank=False)
    name = EncryptedCharField(max_length=200, null=False, blank=False, default="")
    email = models.EmailField(unique=True, null=False, blank=True, default="")
    password  = EncryptedCharField(max_length=50, null=False, blank=False, default="")
    type = models.IntegerField(null=False, blank=False, default=2)
    image = models.ImageField(upload_to="images/hm", blank=True)

    def __str__(self):
        return self.name

    def classname(obj):
        return obj.__class__.__name__

class Candidate(models.Model):
    STATE_CHOICES = (
        (0, "For future revision"),
        (1, "On-hold"),
        (2, "Dropped"),
        (3, "In process - Phone Interview"),
        (4, "In process - Interviewing"),
        (5, "In process - Proposal Sent"),
        (6, "Contracted"),
        (7, "Proposal Rejected")
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = EncryptedCharField(max_length=200, null=False, blank=False, default="")
    email = models.EmailField(unique=True, null=False, blank=True, default="")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = EncryptedCharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    
    linkedin = models.CharField(max_length=200, null=True, blank=True, default="")
    type = models.CharField(max_length=300, null=False, blank=False, default="")
    years_exp = models.IntegerField(null=False, blank=False, default=0)
    enterprise = models.CharField(max_length=100, null=False, blank=True, default="")
    source = models.CharField(max_length=300, null=False, blank=False, default="")
    location = EncryptedCharField(max_length=300, null=False, blank=False, default="")
    status = models.IntegerField(null=False, blank=False, default=0)
    comments = models.CharField(max_length=5000, null=False, blank=True, default="")
    date_added = models.DateTimeField(auto_now_add=True)
    lastupdate = models.DateTimeField(auto_now=True)
    pipeline_comments = models.CharField(max_length=5000, null=False, blank=True, default="")
    responsibleHR = models.ForeignKey(HR, on_delete=models.PROTECT, null=True, related_name="responsibleHR", default="")
    responsibleHM = models.ForeignKey(HiringManager, null=True, on_delete=models.PROTECT, related_name="responsibleHM", default="")
    HiringManager = models.ForeignKey(HiringManager, on_delete=models.PROTECT, default="")
    pipeline_status = models.IntegerField(null=False, blank=False, default=0, choices=STATE_CHOICES)
    pipeline_additional_info = models.CharField(max_length=500, null=False, blank=True, default="")
    last_update_name = models.CharField(max_length=200, null=False, default="")
    image = models.ImageField(upload_to="images/candidate", blank=True)


class CandidateFile(models.Model):
    def upload_function(instance, name):
        """ this function has to return the location to upload the file """
        str_uid = str( instance.user_ref)
        full_path = "docs/candidates/"+str_uid+"/"+name
        return full_path
    
    name = models.CharField(max_length=100, null=False, blank=False, default="")
    pdf = models.FileField(upload_to=upload_function)
    user_ref = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="fileOwner")

