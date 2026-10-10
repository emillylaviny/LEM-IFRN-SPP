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

        user.username = self.cleaned_data['email']

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

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Materiais
        fields = [
            'nome',
            'codigo',
            'descricao',
            'orientacao_uso',
            'conceito_matematico',
            'nivel',
            'series',
            'quantidade',
            'quantidade_disponivel',
            'imagem',
            'localizacao',
            'ativo',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do material',
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código do material',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'orientacao_uso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'conceito_matematico': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nivel': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'series': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
