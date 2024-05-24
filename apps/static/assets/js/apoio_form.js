$(document).ready(function() {
    // Function to hide or show opcao_cur based on tipo_cur checkbox with value 3
    var tipo_cur = document.getElementById("tipo_cur3");
    function toggleOpcaoCur() {
        if ($('input[name="tipo_cur"][value="3"]').is(':checked')) {
            $('#opcao_cur').closest('.form-group').hide();
        } else {
            $('#opcao_cur').closest('.form-group').show();
        }
    }

    // Check the initial state on page load
    toggleOpcaoCur();

    // Bind change event to the checkboxes
    //$('input[name="tipo_cur3"]').on('change', function() {
    //    toggleOpcaoCur();
    //});
    //tipo_cur.addEventListener('change', function () {
    //    toggleOpcaoCur();
    //});
    tipo_cur.addEventListener('input', function(e) {
        toggleOpcaoCur();
    });

});
