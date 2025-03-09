from django import forms
from django.forms import ModelForm
from django.core import validators
from .models import Employer, JobSeeker
from jobAndCompanyActivity_module.models import Job
from iranian_cities.models import Province, County


class RegisterForm(forms.Form):
    """فرم ثبت‌نام برای کاربران جدید."""
    
    first_name = forms.CharField(
        label='نام',
        max_length=120,
        widget=forms.widgets.TextInput(attrs={'class': "input--style-5", 'placeholder': 'نام'})
    )
    
    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=220,
        widget=forms.widgets.TextInput(attrs={'class': "input--style-5", 'placeholder': 'نام خانوادگی'})
    )
    
    email = forms.CharField(
        label='ایمیل',
        widget=forms.widgets.EmailInput(attrs={'class': "input--style-5", 'placeholder': 'ایمیل'})
    )
    
    phone = forms.CharField(
        label='تلفن',
        widget=forms.widgets.TextInput(attrs={'class': "input--style-5", 'placeholder': '09'}),
        validators=[validators.RegexValidator(r"((\+98|0)9\d{9})$", "شماره تلفن معتبر نمی‌باشد")]
    )
    
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.widgets.PasswordInput(attrs={'class': "input--style-5", 'placeholder': 'رمزعبور'}),
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(32)]
    )
    
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.widgets.PasswordInput(attrs={'class': "input--style-5", 'placeholder': 'تکرار رمزعبور'}),
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(32)]
    )
    
    user_type = forms.CharField(
        label='نقش',
        widget=forms.widgets.Select(choices=(('choose', 'انتخاب کنید'), ('employer', 'کارفرما'), ('jobseeker', 'کارجو')))
    )
    
    def clean_confirm_password(self):
        """بررسی تطابق رمز عبور و تکرار آن."""
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError("رمز عبور و تکرار آن مغایرت دارند")
    
    def clean_user_type(self):
        """بررسی انتخاب نوع کاربر."""
        data = self.cleaned_data["user_type"]
        
        if data == 'choose':
            self.add_error('user_type', 'یکی از گزینه‌ها را انتخاب کنید')
            return False
        
        return data


class EmployerRegisterModelForm(ModelForm):
    """فرم ثبت‌نام کارفرما."""
    
    class Meta:
        model = Employer
        exclude = ['user', 'verified_by_admin']
        widgets = {
            'county': forms.Select(attrs={'class': 'form-select', 'onchange': 'Check_county(value)'}),
            'district': forms.Select(attrs={'class': 'form-select', 'disabled': True})
        }


class JobSeekerRegisterForm(ModelForm):
    """فرم ثبت‌نام کارجو."""
    
    class Meta:
        model = JobSeeker
        exclude = ['user']
        widgets = {
            'county': forms.Select(attrs={'class': 'form-select', 'onchange': 'Check_county(value)'}),
            'district': forms.Select(attrs={'class': 'form-select', 'disabled': True})
        }


class ForgotPasswordForm(forms.Form):
    """فرم فراموشی رمز عبور."""
    
    phone = forms.CharField(
        label='تلفن',
        widget=forms.widgets.TextInput(attrs={'class': "input--style-5", 'placeholder': '09'}),
        validators=[validators.RegexValidator(r"((\+98|0)9\d{9})$", "شماره تلفن معتبر نمی‌باشد")]
    )


class ChangePasswordForm(forms.Form):
    """فرم تغییر رمز عبور."""
    
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.widgets.PasswordInput(attrs={'class': "input--style-5", 'placeholder': 'رمزعبور'}),
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(32)]
    )
    
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.widgets.PasswordInput(attrs={'class': "input--style-5", 'placeholder': 'تکرار رمزعبور'}),
        validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(32)]
    )
    
    def clean_confirm_password(self):
        """بررسی تطابق رمز عبور و تکرار آن."""
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError("رمز عبور و تکرار آن مغایرت دارند")


class LoginForm(forms.Form):
    """فرم ورود به سیستم."""
    
    phone = forms.CharField(
        label='تلفن',
        widget=forms.widgets.TextInput(attrs={'class': "input--style-5", 'placeholder': 'شماره تلفن'}),
        validators=[validators.RegexValidator(r"((\+98|0)9\d{9})$", "شماره تلفن معتبر نمی‌باشد")]
    )


class ActiveAccountForm(forms.Form):
    """فرم فعال‌سازی حساب کاربری."""
    
    code = forms.CharField(
        max_length=6,
        min_length=6,
        label="کد فعال‌سازی",
        widget=forms.widgets.TextInput(attrs={
            "id": "activationCode", "class": "form-control text-center",
            "maxlength": "6", "placeholder": "123456"
        })
    )
