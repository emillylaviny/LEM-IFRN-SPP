from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from LEM.forms import MaterialForm, FAQForm
from LEM.models import Materiais, LocalizacaoLab, FAQ

def usuarios(request):
    return render(request, "dashboard/usuarios.html")

def form_usuario(request):
    return render(request, "dashboard/form_usuario.html")

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

