from django.contrib import admin
from gpgrama.models import Admin
from gpgrama.models import HR
from gpgrama.models import HiringManager
from gpgrama.models import Candidate
from gpgrama.models import CandidateFile



# Register your models here.
admin.site.register(Admin)
admin.site.register(HR)
admin.site.register(HiringManager)
admin.site.register(Candidate)
admin.site.register(CandidateFile)