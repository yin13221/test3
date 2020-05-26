from django import forms
from .models import Bbs


class BbsFrom(forms.ModelForm):
    class Meta:
        model = Bbs
        # fields = ["bbs_type", "subject", "content"]
        fields = "__all__"
