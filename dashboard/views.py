from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from LEM.forms import MaterialForm
from LEM.models import Materiais, LocalizacaoLab, FAQ

def usuarios(request):
    return render(request, "dashboard/usuarios.html")

def form_usuario(request):
    return render(request, "dashboard/form_usuario.html")

def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def perguntasfaq(request):
    faqs = FAQ.objects.filter(ativa=True).order_by("ordem", "id")

    context = {
        "faqs": faqs,
    }

    return render(request, "dashboard/perguntasfaq.html", context)

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

    return render(request, "dashboard/materiais.html", context)

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
        "dashboard/form_material.html",
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
        "dashboard/form_material.html",
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
        "dashboard/confirmar_remocao.html",
        {"material": material}
    )

def etiquetas(request):
    return render(request, "dashboard/etiquetas.html")