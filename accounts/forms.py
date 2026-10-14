from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


INPUT_STYLE = (
    "w-full px-4 py-2.5 rounded-xl border border-neutral-300 bg-white "
    "focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 "
    "text-sm text-neutral-900 placeholder-neutral-400 transition-all duration-200"
)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_STYLE, 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': INPUT_STYLE, 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': INPUT_STYLE, 'placeholder': 'Email Address'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': INPUT_STYLE,
                'placeholder': 'Choose a unique username'
            })
            self.fields['username'].help_text = "Letters, digits and @/./+/-/_ only."
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({'class': INPUT_STYLE})
        if 'password_2' in self.fields:
            self.fields['password_2'].widget.attrs.update({'class': INPUT_STYLE})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': INPUT_STYLE,
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': INPUT_STYLE,
            'placeholder': 'Password'
        })


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_STYLE, 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_STYLE, 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': INPUT_STYLE, 'placeholder': 'Email Address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existing = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError("This email address is already in use by another account.")
        return email
