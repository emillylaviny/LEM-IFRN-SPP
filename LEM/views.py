from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import CardMaterialForm
from .models import Card, CadastroUsuario, LocalizacaoLab, Materiais, Emprestimo, Visita, Duvida, FAQ, HistoricoAlteracao
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib import messages


#template - home
def home(request):
    context = {
        "card": Card.objects.all(),
    }
    return render(request, "LEM/home.html", context)

#cadastros
# @login_required
# @permission_required("LEM.add_cadastromateriais")
# def novo_material(request):
#     if request.method == "POST":
#         form = MaterialForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Material cadastrado com sucesso!')
#             return redirect("materiais_lista")
#     else:
#         form = MaterialForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "LEM/form_material.html", context)

def cadastro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    context = {
        "form": form,
    }
    return render(request, "LEM/cadastro_usuario.html", context)

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
# @permission_required("LEM.change_cadastromateriais")
# def editar_material(request, material_id):
#     material = get_object_or_404(CadastroMateriais, id=material_id)
#     if request.method == "POST":
#         form = MaterialForm(request.POST, request.FILES, instance=material)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Material editado com sucesso!')
#             return redirect("materiais_lista")
#     else:
#         form = MaterialForm(instance=material)

#     context = {
#         "form": form,
#         "is_editar": True,
#     }
#     return render(request, "LEM/form_material.html", context)

# @login_required
# @permission_required("LEM.delete_cadastromateriais")
# def remover_material(request, material_id):
#     if request.method == "POST":
#         material = get_object_or_404(CadastroMateriais, id=material_id)
#         material.delete()
#         messages.success(request, 'Material removido com sucesso!')
#         return redirect("materiais_lista")
#     else:
#         return render(request, "LEM/confirmar_remocao.html")

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

# #FAQ - PERGUNTAS FREQUENTES ==========================================
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

# views.py
#
# View responsável por renderizar e processar o formulário de cadastro
# do sistema LEM. O processamento de dados (validação de servidor e
# persistência no banco) está deixado preparado, mas comentado, para
# que possa ser conectado posteriormente ao Model de usuário do LEM.



# template - cadastro de usuario


def cadastro(request):
    """
    Exibe o formulário de cadastro (GET) e processa o envio (POST).
    """
 
    if request.method == 'POST':
        # ------------------------------------------------------------
        # 1. Captura dos dados enviados pelo formulário
        # ------------------------------------------------------------
        nome = request.POST.get('nome', '').strip()
        sobrenome = request.POST.get('sobrenome', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        email = request.POST.get('email', '').strip()
        instituicoes = request.POST.get('instituicoes', '').strip()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')
 
        erros = []
 
        # ------------------------------------------------------------
        # 2. Validação básica no servidor
        #    (a validação "amigável" já acontece no cliente via JS,
        #     mas o servidor nunca deve confiar apenas nisso)
        # ------------------------------------------------------------
        if not nome:
            erros.append('Informe o nome.')
 
        if not sobrenome:
            erros.append('Informe o sobrenome.')
 
        cpf_numeros = ''.join(filter(str.isdigit, cpf))
        if len(cpf_numeros) != 11:
            erros.append('Informe um CPF válido.')
 
        if '@' not in email or '.' not in email:
            erros.append('Informe um e-mail válido.')
 
        if len(senha) < 6:
            erros.append('A senha deve ter no mínimo 6 caracteres.')
        if not re.search(r'[A-Z]', senha):
            erros.append('A senha deve conter ao menos uma letra maiúscula.')
        if not re.search(r'[0-9]', senha):
            erros.append('A senha deve conter ao menos um número.')
        if not re.search(r'[^A-Za-z0-9]', senha):
            erros.append('A senha deve conter ao menos um caractere especial.')
 
        if senha != confirmar_senha:
            erros.append('As senhas não coincidem.')
 
        # ------------------------------------------------------------
        # 3. Se houver erros, retorna ao formulário mantendo os dados
        # ------------------------------------------------------------
        if erros:
            for erro in erros:
                messages.error(request, erro)
 
            contexto = {
                'nome': nome,
                'sobrenome': sobrenome,
                'cpf': cpf,
                'email': email,
                'instituicoes': instituicoes,
            }
            return render(request, 'LEM/cadastro.html', contexto)
 
        # ------------------------------------------------------------
        # 4. Persistência (a implementar junto ao Model de usuário)
        # ------------------------------------------------------------
        # usuario = Usuario.objects.create_user(
        #     nome=nome,
        #     sobrenome=sobrenome,
        #     cpf=cpf_numeros,
        #     email=email,
        #     instituicoes=instituicoes,
        #     password=senha,
        # )
 
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')  # ajustar para a rota real pós-cadastro
 
    # GET: apenas exibe o formulário
    return render(request, 'LEM/cadastro.html')
 