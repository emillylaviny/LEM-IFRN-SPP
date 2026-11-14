from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from LEM.forms import MaterialForm, FAQForm, UsuarioAdminForm
from LEM.models import Materiais, LocalizacaoLab, FAQ, User


@login_required
def usuarios(request):
    lista_usuarios = User.objects.all().order_by("nome_completo")

    return render(
        request,
        "dashboard/usuarios.html",
        {"usuarios": lista_usuarios}
    )


@login_required
def form_usuario(request):
    form = UsuarioAdminForm()

    return render(
        request,
        "dashboard/form_usuario.html",
        {"form": form}
    )


@login_required
def usuario_cadastrar(request):
    if request.method == "POST":
        form = UsuarioAdminForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Usuário cadastrado com sucesso!"
            )
            return redirect("usuarios")

        messages.error(
            request,
            "Não foi possível cadastrar. Verifique os campos."
        )

    else:
        form = UsuarioAdminForm()

    return render(
        request,
        "dashboard/form_usuario.html",
        {"form": form}
    )


@login_required
def usuario_editar(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        form = UsuarioAdminForm(
            request.POST,
            request.FILES,
            instance=usuario
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Usuário atualizado com sucesso!"
            )
            return redirect("usuarios")

        messages.error(
            request,
            "Não foi possível atualizar. Verifique os campos."
        )

    else:
        form = UsuarioAdminForm(instance=usuario)

    return render(
        request,
        "dashboard/form_usuario.html",
        {
            "form": form,
            "usuario": usuario
        }
    )


@login_required
def usuario_excluir(request, id):
    usuario = get_object_or_404(User, id=id)

    if request.method == "POST":
        usuario.delete()
        messages.success(
            request,
            "Usuário excluído com sucesso!"
        )

    return redirect("usuarios")


@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


@login_required
def perguntasfaq(request):
    lista_faqs = FAQ.objects.all().order_by("ordem", "id")

    paginator = Paginator(lista_faqs, 5)
    numero_da_pagina = request.GET.get("pagina", 1)
    faqs = paginator.get_page(numero_da_pagina)

    return render(
        request,
        "dashboard/perguntasfaq.html",
        {"faqs": faqs}
    )


@login_required
def faq_cadastrar(request):
    if request.method == "POST":
        form = FAQForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Pergunta cadastrada com sucesso!"
            )
        else:
            messages.error(
                request,
                "Não foi possível cadastrar. Verifique os campos."
            )

    return redirect("perguntasfaq")


@login_required
def faq_editar(request, id):
    faq = get_object_or_404(FAQ, id=id)

    if request.method == "POST":
        form = FAQForm(request.POST, instance=faq)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Pergunta atualizada com sucesso!"
            )
        else:
            messages.error(
                request,
                "Não foi possível atualizar. Verifique os campos."
            )

    return redirect("perguntasfaq")


@login_required
def faq_excluir(request, id):
    faq = get_object_or_404(FAQ, id=id)

    if request.method == "POST":
        faq.delete()
        messages.success(
            request, "Pergunta excluída com sucesso!"
        )

    return redirect("perguntasfaq")



@login_required
def materiais(request):
    materiais = Materiais.objects.all().order_by("nome")
    form = MaterialForm()
    
    paginator = Paginator(materiais, 5)
    numero_da_pagina = request.GET.get("pagina", 1)
    materiais = paginator.get_page(numero_da_pagina)
    
    return render(
        request,
        "dashboard/materiais.html",
        {
            "materiais": materiais,
            "form_novo": form,
        }
    )


@login_required
def novo_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Material cadastrado com sucesso!"
            )
        else:
            messages.error(
                request,
                "Não foi possível cadastrar. Verifique os campos."
            )

    return redirect("materiais")


@login_required
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
        else:
            messages.error(
                request,
                "Não foi possível atualizar. Verifique os campos."
            )

    return redirect("materiais")


@login_required
def remover_material(request, material_id):
    material = get_object_or_404(
        Materiais,
        id=material_id
    )

    if request.method == "POST":
        material.delete()
        messages.success(
            request,
            "Material excluído com sucesso!"
        )

    return redirect("materiais")

def etiquetas(request):
    return render(request, "dashboard/etiquetas.html")

