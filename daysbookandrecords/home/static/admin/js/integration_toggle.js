(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Function to toggle fieldset visibility based on integration type
        function toggleIntegrationFieldsets() {
            var integrationType = $('#id_integration_type').val();
            
            // Hide all integration fieldsets
            $('.integration-fieldset').each(function() {
                var $fieldset = $(this).closest('fieldset');
                if ($fieldset.length) {
                    $fieldset.hide();
                }
            });
            
            // Show the selected integration's fieldset
            if (integrationType && integrationType !== 'none') {
                var $selectedFieldset = $('.' + integrationType + '-fieldset').closest('fieldset');
                if ($selectedFieldset.length) {
                    $selectedFieldset.show();
                }
            }
        }
        
        // Run on page load
        toggleIntegrationFieldsets();
        
        // Run when integration type changes
        $('#id_integration_type').on('change', function() {
            toggleIntegrationFieldsets();
        });
    });
})(django.jQuery);

