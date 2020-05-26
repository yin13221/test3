from django.forms import ModelForm
from .models import Resource


class ResourceModelForm(ModelForm):
    class Meta:
        model = Resource

        fields = "__all__"
