from django import forms
from .models import Patient
from users.models import CustomUser

class PatientForm(forms.ModelForm):
    #username = forms.CharField(label='Username', required=False)  # Add a read-only field
    class Meta:
        model = Patient
        fields = ['user', 'name', 'age', 'gender', 'address', 'phone_number', 'medical_history']
        exclude = ['created_at']  # Exclude the 'created_at' field from the form
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, user_role=None, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        if user_role:
            self.fields['user'].queryset = CustomUser.objects.filter(role=user_role)
        else:
            self.fields['user'].queryset = CustomUser.objects.all()
        self.fields['user'].label_from_instance = lambda obj: obj.username


        
class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)
    search_by = forms.ChoiceField(label='Search By', choices=[('name', 'Name'), ('id', 'ID'), ('diagnosis', 'Diagnosis')], required=False)