from django import forms
from .models import Doctor
from users.models import CustomUser

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user','name', 'specialty']
    

    def __init__(self, *args, user_role=None, **kwargs):  # Adjust the order of arguments
        super(DoctorForm, self).__init__(*args, **kwargs)
        if user_role:
            self.fields['user'].queryset = CustomUser.objects.filter(role=user_role)
        else:
            self.fields['user'].queryset = CustomUser.objects.all()
        self.fields['user'].label_from_instance = lambda obj: obj.username

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)
    search_by = forms.ChoiceField(label='Search By', choices=[('name', 'Name'), ('id', 'ID'), ('specialty', 'speciality')], required=False)