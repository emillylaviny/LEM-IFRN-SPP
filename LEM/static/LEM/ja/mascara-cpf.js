
document.addEventListener("input", function (event) {
    if (event.target.matches(".cpf-mascara")) {
        const campo = event.target;
        let cpf = campo.value.replace(/\D/g, "").slice(0, 11);

        cpf = cpf.replace(/^(\d{3})(\d)/, "$1.$2");
        cpf = cpf.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
        cpf = cpf.replace(/\.(\d{3})(\d)/, ".$1-$2");

        campo.value = cpf;
    }
});
