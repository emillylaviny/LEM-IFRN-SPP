from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import CardMaterialForm, CadastroForm, MaterialForm, LoginForm
from .models import Card, CadastroUsuario, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, HistoricoAlteracao, FAQ
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError


#template - home
def home(request):
    context = {
        "card": Card.objects.all(),
        "faqs": FAQ.objects.filter(ativa=True).order_by("ordem", "id"),
    }
    return render(request, "LEM/home.html", context)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.error(request, 'Não foi possível concluir o cadastro. Verifique se o CPF e o e-mail já não foram cadastrados.')
            else:
                messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
                return redirect('login')
        else:
            messages.error(request, 'Não foi possível concluir o cadastro. Corrija os itens a seguir:')
            for erros in form.errors.values():
                for erro in erros:
                    messages.error(request, erro)

    else:
        form = CadastroForm()

    return render(request, 'LEM/cadastro.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, "LEM/dashboard.html")

class LoginLEMView(LoginView):
    template_name = 'LEM/login.html'
    authentication_form = LoginForm

    def get(self, request, *args, **kwargs):
        if request.GET.get(self.redirect_field_name) and not request.user.is_authenticated:
            messages.warning(request, 'Faça login para acessar essa página.')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Bem-vindo(a), {form.get_user().first_name}!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'CPF/e-mail ou senha incorretos. Verifique os dados e tente novamente.')
        return super().form_invalid(form)

class LogoutLEMView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(request, 'Você saiu da sua conta. Até logo!')
        return response









#MATERIAIS 

#materiais disponiveis
# def materiais_cadastrados(request):
#     materiais = Materiais.objects.filter(ativo=True)
#     paginator = Paginator(materiais, 10)  # Separa em páginas de 10 materiais
#     numero_da_pagina = request.GET.get('pagina')  # Pega o número da página da URL
#     numero_da_pagina = numero_da_pagina if numero_da_pagina else 1
#     materiais_paginados = paginator.get_page(numero_da_pagina)
#     range_elided = paginator.get_elided_page_range(numero_da_pagina, on_each_side=1, on_ends=1)

#     context = {
    #     "materiais": materiais_paginados,
    #     "range_elided": range_elided,
    # }
    # return render(request, "LEM/materiais_cadastrados.html", context)

#acesso a um material específico do acervo
# def material_informacoes(request, material_id):
#     context = {
#         "material": get_object_or_404(CadastroMateriais, id=material_id),
#     }
#     return render(request, "LEM/material_informacoes.html", context)


# @login_required
# def emprestimo_solicitar(request):
#     if request.method == "POST":
#         form = EmprestimoForm(request.POST)
#         if form.is_valid():
#             emprestimo = form.save(commit=False)
#             emprestimo.professor = request.user
#             emprestimo.save()
#             messages.success(request, 'Empréstimo solicitado com sucesso!')
#             return redirect("meus_emprestimos")
#     else:
#         form = EmprestimoForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "LEM/form_emprestimo.html", context)

# @login_required
# def meus_emprestimos(request):
#     context = {
#         "emprestimos": Emprestimo.objects.filter(professor=request.user).select_related("material"),
#     }
#     return render(request, "LEM/meus_emprestimos.html", context)

#VISITAS 

# @login_required
# def visita_agendar(request):
#     if request.method == "POST":
#         form = VisitaForm(request.POST)
#         if form.is_valid():
#             visita = form.save(commit=False)
#             visita.professor = request.user
#             visita.save()
#             messages.success(request, 'Visita agendada com sucesso!')
#             return redirect("minhas_visitas")
#     else:
#         form = VisitaForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "LEM/visita_agendar.html", context)

# @login_required
# def minhas_visitas(request):
#     context = {
#         "visitas": Visita.objects.filter(professor=request.user),
#     }
#     return render(request, "LEM/minhas_visitas.html", context)

# #FAQ - PERGUNTAS FREQUENTES 
# def faq_lista(request):
#     context = {
#         "faqs": FAQ.objects.filter(ativa=True),
#     }
#     return render(request, "LEM/faq.html", context)


# @login_required
# def duvida_enviar(request):
#     if request.method == "POST":
#         form = DuvidaForm(request.POST)
#         if form.is_valid():
#             duvida = form.save(commit=False)
#             duvida.usuario = request.user
#             duvida.save()
#             return render(request, "LEM/duvida_resposta.html")
#     else:
#         form = DuvidaForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "LEM/duvidas.html", context)

# template - cadastro de usuario


  
 
