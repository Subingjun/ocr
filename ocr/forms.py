from django import forms
from ocr.models import OCRUser, OCRImage


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = OCRUser
        fields = ['username', 'password', 'confirm_password']

    # 验证两次输入的密码是否匹配
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


class OCRImageForm(forms.ModelForm):
    class Meta:
        model = OCRImage
        fields = ['image']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='旧密码')
    new_password = forms.CharField(widget=forms.PasswordInput, label='新密码')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='确认新密码')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("新密码和确认密码不匹配")

        return cleaned_data