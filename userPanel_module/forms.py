from django import forms
from account_module.models import User , Employer , JobSeeker

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class UpdateUserPsswordForm(forms.Form):
    password = forms.CharField(max_length=32,widget=forms.widgets.PasswordInput,label='رمز عبور')
    confirmPassword = forms.CharField(max_length=32,widget=forms.widgets.PasswordInput,label="تکرار رمز عبور")
    
    def clean_Password(self):
        Password = self.cleaned_data.get('Password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        
        if Password != confirmPassword:
            raise forms.ValidationError("رمزعبور و تکرار آن مغایرت دارند")
    
        return Password
        
class UpdateEmployerModelForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ['user','verified_by_admin']
        widgets= {
                'county' :forms.Select(attrs={'onchange':'Check_county(value)'}),
                'district':forms.Select(attrs={'disabled':True})
        }
class UpdateJobSeekerModelForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        exclude = ['user']
        widgets= {
                'county' :forms.Select(attrs={'onchange':'Check_county(value)'}),
                'district':forms.Select(attrs={'disabled':True})
        }
