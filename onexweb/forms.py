from django import forms
from .models import Chapter

class ChapterAdminForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'