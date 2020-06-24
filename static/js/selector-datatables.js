$(document).ready(function(){
        $('#lista_tabla').dataTable();
});

$('#id_seleccionar').on('click', function(){
    $('option', $('#id_estudiante')).attr('selected', 'selected');
});