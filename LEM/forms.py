import re
from datetime import date

from django import forms
from django.contrib.auth.hashers import make_password

from .models import (
    CadastroUsuario,
    CadastroMateriais,
    Emprestimo,
    Visita,
    Duvida,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BOOTSTRAP_TEXT_CLASSES = "form-control"
BOOTSTRAP_FILE_CLASSES = "form-control"
BOOTSTRAP_SELECT_CLASSES = "form-select"


def _texto(placeholder="", **extra):
    attrs = {"class": BOOTSTRAP_TEXT_CLASSES, "placeholder": placeholder}
    attrs.update(extra)
    return forms.TextInput(attrs=attrs)


def _cpf_apenas_digitos(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")


# ---------------------------------------------------------------------------
# Cadastro de usuário (professor)
# ---------------------------------------------------------------------------

class UserCreationForm(forms.ModelForm):
    """
    Form de cadastro público de usuário (professor).

    Observação: como o modelo CadastroUsuario NÃO é o AUTH_USER_MODEL do
    projeto, este form apenas grava o registro na tabela CadastroUsuario.
    Ele não autentica ninguém e não integra com django.contrib.auth — isso
    precisa ser resolvido na camada de views/autenticação (ver aviso acima).
    """

    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": BOOTSTRAP_TEXT_CLASSES,
            "placeholder": "Digite uma senha",
        }),
        min_length=8,
        help_text="Mínimo de 8 caracteres.",
    )
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={
            "class": BOOTSTRAP_TEXT_CLASSES,
            "placeholder": "Repita a senha",
        }),
    )

    class Meta:
        model = CadastroUsuario
        fields = [
            "nome_completo",
            "apelido",
            "cpf",
            "data_nascimento",
            "foto",
            "escola",
            "declaracao_escola",
            "cidade_escola",
            "email",
            "telefone",
            "cidade_residencia",
            "senha",
        ]
        widgets = {
            "nome_completo": _texto("Nome completo"),
            "apelido": _texto("Apelido (opcional)"),
            "cpf": _texto("000.000.000-00"),
            "data_nascimento": forms.DateInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "type": "date"}
            ),
            "foto": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE_CLASSES}),
            "escola": _texto("Escola onde leciona"),
            "declaracao_escola": forms.ClearableFileInput(
                attrs={"class": BOOTSTRAP_FILE_CLASSES}
            ),
            "cidade_escola": _texto("Cidade da escola"),
            "email": forms.EmailInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "placeholder": "seuemail@exemplo.com"}
            ),
            "telefone": _texto("(00) 00000-0000"),
            "cidade_residencia": _texto("Cidade onde reside"),
        }
        labels = {
            "nome_completo": "Nome completo",
            "apelido": "Apelido",
            "cpf": "CPF",
            "data_nascimento": "Data de nascimento",
            "foto": "Foto",
            "escola": "Escola",
            "declaracao_escola": "Declaração da escola",
            "cidade_escola": "Cidade da escola",
            "email": "E-mail",
            "telefone": "Telefone",
            "cidade_residencia": "Cidade de residência",
        }

    def clean_cpf(self):
        cpf = _cpf_apenas_digitos(self.cleaned_data.get("cpf", ""))
        if len(cpf) != 11:
            raise forms.ValidationError("Informe um CPF válido, com 11 dígitos.")
        if cpf == cpf[0] * 11:
            raise forms.ValidationError("CPF inválido.")

        qs = CadastroUsuario.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe um usuário cadastrado com este CPF.")

        # Grava formatado, igual ao padrão usado no restante do sistema.
        return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        qs = CadastroUsuario.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe um usuário cadastrado com este e-mail.")
        return email

    def clean_data_nascimento(self):
        nascimento = self.cleaned_data.get("data_nascimento")
        if nascimento and nascimento > date.today():
            raise forms.ValidationError("A data de nascimento não pode estar no futuro.")
        return nascimento

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error("confirmar_senha", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.senha = make_password(self.cleaned_data["senha"])
        if commit:
            usuario.save()
        return usuario


# ---------------------------------------------------------------------------
# Materiais do acervo
# ---------------------------------------------------------------------------

class MaterialForm(forms.ModelForm):
    class Meta:
        model = CadastroMateriais
        fields = [
            "nome",
            "codigo",
            "descricao",
            "orientacao_uso",
            "conceito_matematico",
            "nivel",
            "series",
            "quantidade",
            "quantidade_disponivel",
            "imagem",
            "localizacao",
            "ativo",
        ]
        widgets = {
            "nome": _texto("Nome do material"),
            "codigo": _texto("Código de identificação"),
            "descricao": forms.Textarea(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "rows": 4,
                       "placeholder": "Descrição do material"}
            ),
            "orientacao_uso": forms.Textarea(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "rows": 4,
                       "placeholder": "Como utilizar o material"}
            ),
            "conceito_matematico": _texto("Ex.: Geometria, Álgebra..."),
            "nivel": _texto("Ex.: Fundamental, Médio..."),
            "series": _texto("Ex.: 6º ao 9º ano"),
            "quantidade": forms.NumberInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "min": 1}
            ),
            "quantidade_disponivel": forms.NumberInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "min": 0}
            ),
            "imagem": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE_CLASSES}),
            "localizacao": forms.Select(attrs={"class": BOOTSTRAP_SELECT_CLASSES}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nome": "Nome",
            "codigo": "Código",
            "descricao": "Descrição",
            "orientacao_uso": "Orientação de uso",
            "conceito_matematico": "Conceito matemático",
            "nivel": "Nível de ensino",
            "series": "Séries",
            "quantidade": "Quantidade total",
            "quantidade_disponivel": "Quantidade disponível",
            "imagem": "Imagem",
            "localizacao": "Localização no laboratório",
            "ativo": "Ativo",
        }

    def clean(self):
        cleaned_data = super().clean()
        quantidade = cleaned_data.get("quantidade")
        quantidade_disponivel = cleaned_data.get("quantidade_disponivel")
        if (
            quantidade is not None
            and quantidade_disponivel is not None
            and quantidade_disponivel > quantidade
        ):
            self.add_error(
                "quantidade_disponivel",
                "A quantidade disponível não pode ser maior que a quantidade total.",
            )
        return cleaned_data


# ---------------------------------------------------------------------------
# Empréstimos
# ---------------------------------------------------------------------------

class EmprestimoForm(forms.ModelForm):
    """
    O campo `professor` é preenchido na view (a partir do usuário logado),
    por isso não aparece aqui. `status` também fica de fora: quem solicita
    não deve poder se autoaprovar.
    """

    class Meta:
        model = Emprestimo
        fields = [
            "material",
            "quantidade",
            "data_retirada",
            "data_devolucao_prevista",
            "observacao",
        ]
        widgets = {
            "material": forms.Select(attrs={"class": BOOTSTRAP_SELECT_CLASSES}),
            "quantidade": forms.NumberInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "min": 1}
            ),
            "data_retirada": forms.DateInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "type": "date"}
            ),
            "data_devolucao_prevista": forms.DateInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "type": "date"}
            ),
            "observacao": forms.Textarea(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "rows": 3,
                       "placeholder": "Observações (opcional)"}
            ),
        }
        labels = {
            "material": "Material",
            "quantidade": "Quantidade",
            "data_retirada": "Data de retirada",
            "data_devolucao_prevista": "Data prevista de devolução",
            "observacao": "Observação",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só oferece materiais ativos e com estoque disponível.
        self.fields["material"].queryset = CadastroMateriais.objects.filter(
            ativo=True, quantidade_disponivel__gt=0
        )

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get("material")
        quantidade = cleaned_data.get("quantidade")
        data_retirada = cleaned_data.get("data_retirada")
        data_devolucao_prevista = cleaned_data.get("data_devolucao_prevista")

        if material and quantidade and quantidade > material.quantidade_disponivel:
            self.add_error(
                "quantidade",
                f"Só há {material.quantidade_disponivel} unidade(s) disponível(is) "
                f"para este material.",
            )

        if data_retirada and data_retirada < date.today():
            self.add_error("data_retirada", "A data de retirada não pode estar no passado.")

        if (
            data_retirada
            and data_devolucao_prevista
            and data_devolucao_prevista < data_retirada
        ):
            self.add_error(
                "data_devolucao_prevista",
                "A data de devolução prevista não pode ser anterior à data de retirada.",
            )

        return cleaned_data


# ---------------------------------------------------------------------------
# Visitas
# ---------------------------------------------------------------------------

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = [
            "data",
            "horario",
            "quantidade_visitantes",
            "finalidade",
            "observacao",
        ]
        widgets = {
            "data": forms.DateInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "type": "date"}
            ),
            "horario": forms.TimeInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "type": "time"}
            ),
            "quantidade_visitantes": forms.NumberInput(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "min": 1}
            ),
            "finalidade": forms.Textarea(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "rows": 3,
                       "placeholder": "Qual o objetivo da visita?"}
            ),
            "observacao": forms.Textarea(
                attrs={"class": BOOTSTRAP_TEXT_CLASSES, "rows": 3,
                       "placeholder": "Observações (opcional)"}
            ),
        }
        labels = {
            "data": "Data da visita",
            "horario": "Horário",
            "quantidade_visitantes": "Quantidade de visitantes",
            "finalidade": "Finalidade",
            "observacao": "Observação",
        }

    def clean_data(self):
        data_visita = self.cleaned_data.get("data")
        if data_visita and data_visita < date.today():
            raise forms.ValidationError("A data da visita não pode estar no passado.")
        return data_visita


# ---------------------------------------------------------------------------
# Dúvidas
# ---------------------------------------------------------------------------

class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ["pergunta"]
        widgets = {
            "pergunta": forms.Textarea(
                attrs={
                    "class": BOOTSTRAP_TEXT_CLASSES,
                    "rows": 4,
                    "placeholder": "Digite sua dúvida...",
                }
            ),
        }
        labels = {
            "pergunta": "Sua dúvida",
        }

    def clean_pergunta(self):
        pergunta = self.cleaned_data.get("pergunta", "").strip()
        if len(pergunta) < 10:
            raise forms.ValidationError(
                "Descreva sua dúvida com um pouco mais de detalhe (mínimo 10 caracteres)."
            )
        return pergunta