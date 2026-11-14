import re
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Materiais, User, FAQ
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class CadastroForm(UserCreationForm):
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(label='E-mail') 

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

        if len(cpf) != 11:
            raise forms.ValidationError('Informe um CPF com 11 dígitos.')

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


class UsuarioAdminForm(forms.ModelForm):

    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        min_length=8,
        required=False
    )

    confirmacao_senha = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "nome_completo",
            "apelido",
            "cpf",
            "data_nascimento",
            "foto",
            "cidade_residencia",
            "escola",
            "cidade_escola",
            "declaracao_escola",
            "email",
            "telefone",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["senha"].required = False
            self.fields["confirmacao_senha"].required = False

    def clean_cpf(self):
        cpf = re.sub(r"\D", "", self.cleaned_data["cpf"])

        if len(cpf) != 11:
            raise forms.ValidationError(
                "Informe um CPF com 11 dígitos."
            )

        usuarios = User.objects.filter(cpf=cpf)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                "Já existe um usuário com este CPF."
            )

        return cpf

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        usuarios = User.objects.filter(email__iexact=email)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                "Já existe um usuário com este e-mail."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        senha = cleaned_data.get("senha")
        confirmacao = cleaned_data.get("confirmacao_senha")

        if not self.instance.pk and not senha:
            self.add_error("senha", "Informe uma senha.")

        if senha and senha != confirmacao:
            self.add_error(
                "confirmacao_senha",
                "As senhas não coincidem."
            )

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)

        if not usuario.pk:
            usuario.username = uuid.uuid4().hex

        senha = self.cleaned_data.get("senha")

        if senha:
            usuario.set_password(senha)

        if not usuario.vinculo_profissional:
            usuario.vinculo_profissional = "Não informado"

        if commit:
            usuario.save()

        return usuario

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

