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
    faqs = FAQ.objects.all().order_by("ordem", "id")

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