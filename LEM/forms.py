from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Materiais, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class CadastroForm(UserCreationForm):
    username = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'cpf',
            'vinculo_profissional',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['first_name']

        if commit:
            user.save()

        return user

class CardMaterialForm(forms.ModelForm):
    class Meta:
        model = Materiais
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column('imagem', css_class='col-md-12'),
            ),
            Row(
                Column('titulo', css_class='col-md-12'),
            ),
            Row(
                Column('descricao', css_class='col-md-12'),
            ),
            Submit(
                'submit',
                'Salvar',
                css_class='btn btn-primary'
            )
        )