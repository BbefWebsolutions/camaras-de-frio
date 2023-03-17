function abrirCargando() {
    $("#cargandoInformacion").modal({
        backdrop: 'static',
        keyboard: false,
        show: false
    });
    $("#cargandoInformacion").modal("show");
}

function cerrarCargando() {
    $("#cargandoInformacion").modal("hide");
}