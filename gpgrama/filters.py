from django_filters import FilterSet

from gpgrama.models import Candidate


class CandidateFilter(FilterSet):
    class Meta:
        model = Candidate
        fields = {
            'name': ['icontains'],
            'type': ['exact'],
            'status': ['exact'],
            'years_exp': ['exact'],
            'responsibleHR':['exact'],
            'responsibleHM':['exact']
        } 

class CandidatePipelineFilter(FilterSet):
    class Meta:
        model = Candidate
        fields = {'pipeline_comments': ['icontains'],
                  'pipeline_status': ['exact']
                  }

