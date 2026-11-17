from django.db import migrations

INSTITUICOES = [
    "Colégio São José",
    "Sociedade Educadora São Franscisco",
    "Escola Estadual Maurício Freire",
    "Escola Estadual Djalma Marinho",
    "Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte",
    "Outra",
]


def criar_instituicoes(apps, schema_editor):
    Instituicao = apps.get_model("LEM", "Instituicao")
    for nome in INSTITUICOES:
        Instituicao.objects.get_or_create(nome=nome, defaults={"ativa": True})


class Migration(migrations.Migration):

    dependencies = [
        ('LEM', '0006_remove_user_escola_remove_user_is_admin_and_more'),
    ]

    operations = [
        migrations.RunPython(criar_instituicoes, migrations.RunPython.noop),
    ]