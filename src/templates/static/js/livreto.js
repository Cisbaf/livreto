
var livretoModal;
var livretoDiv;

function RegisterLivreto(url) {
    const form = livretoDiv.querySelector("form");
    const title = form.querySelector("h1");
    const fname = form.querySelector("#fname");
    const fdesc = form.querySelector("#fdesc");
    title.innerHTML = "Registrar Livreto";
    form.action = url;
    fname.value = "";
    fdesc.value = "";
    livretoModal.show();
}

function EditLivreto(pk, url, name, desc, system, urlDel) {
    const form = livretoDiv.querySelector("form");
    const title = form.querySelector("h1");
    const fname = form.querySelector("#fname");
    const fdesc = form.querySelector("#fdesc");
    const options = form.querySelectorAll("option");
    const btnDel = form.querySelector("#btndel");
    title.innerHTML = "Editar Livreto";
    form.action = url;
    fname.value = name;
    fdesc.value = desc;
    btnDel.onclick = ()=> DeleteLivreto(urlDel, name);
    for (var x = 0; x < options.length; x ++){
        const option = options[x];
        if (option.value == system){
            option.selected = true;
        }
    }
    livretoModal.show();
}

function DeleteLivreto(urlDel, name) {
    const del = confirm(`Você realmente deseja deletar o livreto ${name} ?`)
    if (!del) return;
    window.location = urlDel;
}


window.addEventListener("DOMContentLoaded", ()=>{
    livretoDiv = document.getElementById('livretoModal');
    livretoModal = new bootstrap.Modal(livretoDiv);
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
});