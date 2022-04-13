from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].required = True
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']

    # 이메일 중복 막기
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('이미 등록된 email입니다')
        return email

class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'gender', 'phone_number', 'first_name', 'last_name', 'email', 'website_url', 'bio']