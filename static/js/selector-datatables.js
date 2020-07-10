$(document).ready(function(){
        $('#lista_tabla').dataTable();
});

$(document).ready(function(){
	$('#id_seleccionar').on('change', function(){
		if($(this).is(':checked'))
		{
			$('option', $('#id_estudiante')).attr('selected', 'selected');
		}
	    else
	    {
	    	$('option', $('#id_estudiante')).removeAttr('selected')
	    }
	});
});