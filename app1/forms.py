from django import forms
from .models import Ticket

class ChatbotForm(forms.Form):
    hw_type = forms.ChoiceField(
        label='Hardware Type',
        choices=[],  # Choices will be set in the view
        required=True
    )
    apps_sw = forms.ChoiceField(
        label='Software/Application',
        choices=[],
        required=True
    )
    report_type = forms.ChoiceField(
        label='Report Type',
        choices=[],
        required=True
    )
    report_desc = forms.CharField(
        label='Problem Description',
        widget=forms.Textarea,
        required=True
    )
    pc_ip = forms.CharField(
        label='PC IP Address',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(ChatbotForm, self).__init__(*args, **kwargs)
        self.fields['hw_type'].choices = self.get_distinct_choices('hw_type')
        self.fields['apps_sw'].choices = self.get_distinct_choices('apps_sw')
        self.fields['report_type'].choices = self.get_distinct_choices('report_type')

    def get_distinct_choices(self, field_name):
        distinct_values = Ticket.objects.values_list(field_name, flat=True).distinct()
        return [(value, value) for value in distinct_values if value]
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False, initial=False, label='Admin')
    is_technician = forms.BooleanField(required=False, initial=False, label='Technician')
    is_user = forms.BooleanField(required=False, initial=True, label='User')  # Default to User

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'is_admin', 'is_technician', 'is_user')

    def clean(self):
        cleaned_data = super().clean()
        is_admin = cleaned_data.get('is_admin')
        is_technician = cleaned_data.get('is_technician')
        is_user = cleaned_data.get('is_user')

        if sum([bool(is_admin), bool(is_technician), bool(is_user)]) != 1:
            raise forms.ValidationError("You must select exactly one role.")

        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')




# forms.py
# forms.py


