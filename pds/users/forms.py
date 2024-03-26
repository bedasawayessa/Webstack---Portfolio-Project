from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserRegistrationForm(UserCreationForm):
    
    # Add additional fields here
    email = forms.EmailField(max_length = 254, help_text = "Unique Email")
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'name', 'role']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            users = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % users)

    def __init__(self, *args, user_role=None, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if user_role:
            self.fields['username'].queryset = CustomUser.objects.filter(role=user_role)
        else:
            self.fields['username'].queryset = CustomUser.objects.all()
        self.fields['username'].label_from_instance = lambda obj: obj.username

class UserChangeForm(UserChangeForm):
    
    email = forms.EmailField(max_length=254, help_text="Unique Email")

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'name', 'role']

# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = ('email', )


class UserLoginForm(forms.ModelForm):
    # Add additional fields here
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password',]

    def clean(self):
        # cleaned_data = super().clean()

        # email = cleaned_data.get('email')
        # password = cleaned_data.get('password')
        
        # if email and password:
        #     user = authenticate(email=email, password=password)
        #     if not user:
        #         raise forms.ValidationError("Invalid Email or Password")
        # return cleaned_data
         #super().clean()  # Perform default form validation
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Email or Password ")
            
            if not CustomUser.objects.filter(email= email).exists():
                #raise forms.ValidationError("Invalid email address")
                raise forms.ValidationError('Email "%s" is Doesn\'t in use.' % email)
            #return email

        
class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', required=False)
    search_by = forms.ChoiceField(label='Search By', choices=[('username', 'Username'), ('id', 'ID'), ('role', 'Roles')], required=False)