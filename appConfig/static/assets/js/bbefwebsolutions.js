$(document).ready(function () {    
    $('.numberonly').keypress(function (e) {    
        var charCode = (e.which) ? e.which : event.keyCode
        if (String.fromCharCode(charCode).match(/[^0-9]/g))
            return false;
    });  

    
    $('.nav-tabs a').click(function (link) {
        $(".dx-widget").each(function(a,b) {
            grid = "#"+b.id
            if(grid!="#" && grid!="#ganttProyecto")
            {   
                $(grid).dxDataGrid("instance").refresh();                  
                $(grid).dxDataGrid("instance").updateDimensions();
            }
        });
    })
});


$(function () {
  'use strict'

  $('a.nav-link').click(function(){
    if($(this).data('autoload')){
        var url = $(this).data("url");
        if (typeof url !== "undefined") {
            var pane = $(this), href = this.hash;
            $(href).load(url, function (result, status, xhr) {
                pane.tab('show');
            });
        } else {
            $(this).tab('show');
        }
    }
})
  
  $('.nav li.nav-item.with-sub ul li a').on('click', function (e) {
    abrirCargando();
  });

  $.fn.serializeObject = function() {
      var o = {};
      var a = this.serializeArray();
      $.each(a, function() {
          if (o[this.name]) {
              if (!o[this.name].push) {
                  o[this.name] = [o[this.name]];
              }
              o[this.name].push(this.value || '');
          } else {
              o[this.name] = this.value || '';
          }
      });
      return o;
  };

});

$(document).ready(function () {
    cerrarCargando();

});

function number_format(amount, decimals) {

    amount += ''; // por si pasan un numero en vez de un string
    amount = parseFloat(amount.replace(/[^0-9\.]/g, '')); // elimino cualquier cosa que no sea numero o punto

    decimals = decimals || 0; // por si la variable no fue fue pasada

    // si no es un numero o es igual a cero retorno el mismo cero
    if (isNaN(amount) || amount === 0) 
        return parseFloat(0).toFixed(decimals);

    // si es mayor o menor que cero retorno el valor formateado como numero
    amount = '' + amount.toFixed(decimals);

    var amount_parts = amount.split('.'),
        regexp = /(\d+)(\d{3})/;

    while (regexp.test(amount_parts[0]))
        amount_parts[0] = amount_parts[0].replace(regexp, '$1' + '.' + '$2');
    
    return amount_parts.join('.')
}

function acortarSelect(id, limite = 30) {
    $("#" + id + " > option").each(function () {
        $(this).attr('title', this.text);
        if (this.text.length > limite) { 
            this.text = this.text.slice(0, limite) + '...'; }
    });
}

function submitFormulario(id_formulario) {
    let formulario = $('#'+id_formulario).parsley()
    if (formulario.validate()) {
      abrirCargando();
      $('#'+id_formulario).submit();
    }
    else {
      formulario.refresh();
      const titulo = 'Formulario incompleto!';
      const mensaje = 'Te ha faltado algo en el formulario.\nRevisa el formulario';
      notify = new PNotify({
        title: titulo,
        text: mensaje,
        type: 'error',
        styling: 'bootstrap3',
        delay: 3000
      });
    }
  }

  function visibleDataGrid(){ 
    if('{{propuesta.estado.id}}' == 1){
        return true
    } else {
        return false}
    } 

  function estadoFila(estado){
    if(estado==true){
      _on = "fas fa-toggle-on"
      return _on
    }else{
      _off = "fas fa-toggle-off"
      return _off
    }
  }
  
  function desactivarFila(estado){
    _disabled = "disabledRow"
    if(estadoHito){
      disabled = ""
    }
    return disabled;
  }

  function desactivarBotones(estado){
      if(estado){
          return true
      }else{
        return false
      }
  }


