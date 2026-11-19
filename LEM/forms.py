import re
import json
import uuid
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Materiais, User, FAQ, Duvida, Instituicao
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
    username = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    cpf = forms.CharField(
        label='CPF',
        max_length=14
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={
            'invalid': 'Digite um e-mail válido, por exemplo: nome@exemplo.com',
            'required': 'Informe seu e-mail.',
        }
    )

    # Campo onde o usuário digitará as instituições separadas por vírgula
    vinculos_profissionais_texto = forms.CharField(
        label='Instituição(ões) onde trabalha',
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'id_vinculos_profissionais_texto',
            'placeholder': 'Digite o nome da instituição',
            'autocomplete': 'off',
        })
    )

    # Receberá as cidades das instituições ainda não cadastradas
    instituicoes_cidades = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    historico_escola = forms.FileField(
        label='Histórico da escola',
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'cpf',
            'historico_escola',
        ]

    def clean_cpf(self):
        cpf = re.sub(r'\D', '', self.cleaned_data['cpf'])

        if not cpf_valido(cpf):
            raise forms.ValidationError('CPF inválido.')

        usuarios = User.objects.filter(cpf=cpf)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                'Já existe um usuário cadastrado com este CPF.'
            )

        return cpf

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        usuarios = User.objects.filter(email__iexact=email)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                'Já existe um usuário cadastrado com este e-mail.'
            )

        return email

    def clean_historico_escola(self):
        arquivo = self.cleaned_data.get('historico_escola')

        if not arquivo:
            raise forms.ValidationError(
                'Anexe o histórico de uma das escolas.'
            )

        extensoes = ('.pdf', '.jpg', '.jpeg', '.png')

        if not arquivo.name.lower().endswith(extensoes):
            raise forms.ValidationError(
                'Envie um arquivo PDF, JPG ou PNG.'
            )

        if arquivo.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                'O arquivo pode ter no máximo 5 MB.'
            )

        return arquivo

    def clean(self):
        cleaned_data = super().clean()

        texto = cleaned_data.get(
            'vinculos_profissionais_texto', ''
        ).strip()

        cidades_json = cleaned_data.get(
            'instituicoes_cidades', ''
        )

        try:
            cidades = json.loads(cidades_json or '{}')

            if not isinstance(cidades, dict):
                raise ValueError

        except (ValueError, TypeError):
            self.add_error(
                'instituicoes_cidades',
                'Não foi possível identificar as cidades das instituições.'
            )
            return cleaned_data

        # Separa as instituições pela vírgula e remove espaços extras
        nomes = [
            nome.strip()
            for nome in texto.split(',')
            if nome.strip()
        ]

        # Evita nomes repetidos na mesma inscrição
        nomes_unicos = []
        nomes_vistos = set()

        for nome in nomes:
            chave = nome.casefold()

            if chave not in nomes_vistos:
                nomes_unicos.append(nome)
                nomes_vistos.add(chave)

        if not nomes_unicos:
            self.add_error(
                'vinculos_profissionais_texto',
                'Informe pelo menos uma instituição.'
            )
            return cleaned_data

        instituicoes_processadas = []

        for nome in nomes_unicos:
            instituicao = Instituicao.objects.filter(
                nome__iexact=nome
            ).first()

            if instituicao:
                instituicoes_processadas.append({
                    'nome': instituicao.nome,
                    'cidade': instituicao.cidade_escola,
                })

            else:
                cidade = str(
                    cidades.get(nome, '')
                ).strip()

                if not cidade:
                    self.add_error(
                        'vinculos_profissionais_texto',
                        f'Informe a cidade da nova instituição: {nome}.'
                    )
                    continue

                instituicoes_processadas.append({
                    'nome': nome,
                    'cidade': cidade,
                })

        cleaned_data['instituicoes_processadas'] = (
            instituicoes_processadas
        )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = uuid.uuid4().hex

        primeiro_nome = self.cleaned_data.get(
            'first_name', ''
        ).strip()

        ultimo_nome = self.cleaned_data.get(
            'last_name', ''
        ).strip()

        user.nome_completo = (
            f"{primeiro_nome} {ultimo_nome}"
        ).strip()

        if commit:
            user.save()

            escolas = []

            for dados in self.cleaned_data.get(
                'instituicoes_processadas', []
            ):
                escola = Instituicao.objects.filter(
                    nome__iexact=dados['nome']
                ).first()

                if not escola:
                    escola = Instituicao.objects.create(
                        nome=dados['nome'],
                        cidade_escola=dados['cidade'],
                        ativa=True
                    )

                escolas.append(escola)

            user.vinculos_profissionais.set(escolas)

            user.vinculo_profissional = ', '.join(
                escola.nome for escola in escolas
            )

            user.save(
                update_fields=['vinculo_profissional']
            )

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

    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs={
            "class": "form-control cpf-mascara",
            "placeholder": "000.000.000-00",
            "maxlength": "14",
            "inputmode": "numeric",
        })
    )

    email = forms.EmailField(
        label="E-mail",
        error_messages={
            "invalid": "Digite um e-mail válido, por exemplo: nome@exemplo.com",
            "required": "Informe seu e-mail.",
        }
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
            "vinculo_profissional",
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

            cpf = re.sub(r"\D", "", self.instance.cpf or "")
            if len(cpf) == 11:
                self.initial["cpf"] = (
                    f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                )

    def clean_cpf(self):
        cpf = re.sub(r"\D", "", self.cleaned_data["cpf"])

        if not cpf_valido(cpf):
            raise forms.ValidationError("CPF inválido.")

        usuarios = User.objects.filter(cpf=cpf)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                "Já existe um usuário cadastrado com este CPF."
            )

        return cpf

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        usuarios = User.objects.filter(email__iexact=email)

        if self.instance and self.instance.pk:
            usuarios = usuarios.exclude(pk=self.instance.pk)

        if usuarios.exists():
            raise forms.ValidationError(
                "Já existe um usuário cadastrado com este e-mail."
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

class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ["pergunta"]
        labels = {"pergunta": "Sua pergunta"}
        widgets = {
            "pergunta": forms.Textarea(attrs={
                "rows": 5,
                "class": "form-control dv-textarea",
                "placeholder": "Escreva aqui a sua dúvida...",
            }),
        }

    def clean_pergunta(self):
        pergunta = self.cleaned_data["pergunta"].strip()
        if len(pergunta) < 10:
            raise forms.ValidationError("Escreva a sua dúvida com pelo menos 10 caracteres.")
        if len(pergunta) > 1000:
            raise forms.ValidationError("A pergunta pode ter no máximo 1000 caracteres.")
        return pergunta
    
    
class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = [
            "nome",
            "cidade_escola",
            "ativa",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome da escola",
            }),

            "cidade_escola": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Cidade da escola",
            }),
        }

        labels = {
            "nome": "Nome da escola",
            "cidade_escola": "Cidade",
            "ativa": "Instituição ativa",
        }