$(document).ready(function() {
    // Function to hide or show opcao_cur based on tipo_cur checkbox with value 3
    function toggleOpcaoCur() {
        console.log("Checking the state of the checkboxes...");
        if ($('input[name="tipo_cur"][value="3"]').is(':checked')) {
            console.log("Checkbox with value 3 is checked. Hiding opcao_cur...");
            $('#opcao_cur').closest('.form-group').hide();
        } else {
            console.log("Checkbox with value 3 is not checked. Showing opcao_cur...");
            $('#opcao_cur').closest('.form-group').show();
        }
    }

    // Check the initial state on page load
    toggleOpcaoCur();

    // Bind change event to the checkboxes
    $('input[name="tipo_cur"]').on('change', function() {
        console.log("Checkbox state changed. Rechecking...");
        toggleOpcaoCur();
    });
});