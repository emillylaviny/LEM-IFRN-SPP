import re
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import CardMaterialForm, CadastroForm, MaterialForm
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

def usuarios(request):
    return render(request, "LEM/usuarios.html")

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')

    else:
        form = CadastroForm()

    return render(request, 'LEM/cadastro.html', {'form': form})


def dashboard(request):
    return render(request, "LEM/dashboard.html")

def perguntasfaq(request):
    return render(request, "LEM/perguntasfaq.html")


def materiais(request):
    lista_materiais = Materiais.objects.select_related(
        "localizacao"
    ).all()

    context = {
        "materiais": lista_materiais,
        "niveis": lista_materiais
            .exclude(nivel="")
            .values_list("nivel", flat=True)
            .distinct(),
        "localizacoes": LocalizacaoLab.objects.all(),
    }

    return render(request, "LEM/materiais.html", context)

@login_required
# @permission_required("LEM.add_cadastromateriais")
def novo_material(request):
    if request.method == "POST":
        form = MaterialForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Material cadastrado com sucesso!"
            )
            return redirect("materiais")
    else:
        form = MaterialForm()

    return render(
        request,
        "LEM/form_material.html",
        {
            "form": form,
            "titulo": "Cadastrar material",
        }
    )

@login_required
# @permission_required("LEM.change_cadastromateriais")
def editar_material(request, material_id):
    material = get_object_or_404(
        Materiais,
        id=material_id
    )

    if request.method == "POST":
        form = MaterialForm(
            request.POST,
            request.FILES,
            instance=material
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Material atualizado com sucesso!"
            )
            return redirect("materiais")
    else:
        form = MaterialForm(instance=material)

    return render(
        request,
        "LEM/form_material.html",
        {
            "form": form,
            "material": material,
            "titulo": "Editar material",
        }
    )

@login_required
# @permission_required("LEM.change_cadastromateriais")
def remover_material(request, material_id):
    material = get_object_or_404(
        Materiais,
        id=material_id
    )

    if request.method == "POST":
        material.delete()
        messages.success(
            request,
            "Material removido com sucesso!"
        )
        return redirect("materiais")

    return render(
        request,
        "LEM/confirmar_remocao.html",
        {"material": material}
    )






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


  
 
