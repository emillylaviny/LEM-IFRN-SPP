import re
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Materiais, User, FAQ
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

def cpf_valido(cpf):
    # Rejeita sequências como 111.111.111-11
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in (9, 10):
        soma = sum(int(cpf[n]) * (i + 1 - n) for n in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

class CadastroForm(UserCreationForm):
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    cpf = forms.CharField(label='CPF', max_length=14)
    email = forms.EmailField(label='E-mail', error_messages={
        'invalid': 'Digite um e-mail válido, por exemplo: nome@exemplo.com',
        'required': 'Informe seu e-mail.',
    })

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'cpf',
            'vinculo_profissional',
        ]

    def clean_cpf(self):
        cpf = re.sub(r'\D', '', self.cleaned_data['cpf']) 

        if not cpf_valido(cpf):
            raise forms.ValidationError('CPF inválido.')

        if User.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este CPF.')

        return cpf

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este e-mail.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = uuid.uuid4().hex 

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    """Login por CPF ou e-mail"""

    def clean(self):
        identificador = (self.cleaned_data.get('username') or '').strip()

        if identificador:
            if '@' in identificador:
                usuarios = User.objects.filter(email__iexact=identificador)
            else:
                cpf = re.sub(r'\D', '', identificador)   # aceita com ou sem pontos
                usuarios = User.objects.filter(cpf=cpf) if cpf else User.objects.none()

            if usuarios.count() == 1:
                self.cleaned_data['username'] = usuarios.first().username

        return super().clean()

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
        
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = [
            "pergunta", 
            "resposta", 
            "ativa", 
            "ordem"
        ]

