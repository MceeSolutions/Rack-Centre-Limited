odoo.define('rc_cc_material_gatepass.material_gatepass', function(require){
    
    'use_strict';
    
    $('#add-more-materials').click(function(e) {
        e.preventDefault();
        var Row = $("<div class='row'></div>");
        var col = $("<div class='form-group s_website_form_field col-12 s_website_form_required col-lg-4' data-type='char' data-name='Field'></div>");
        $('<input type="text" class="form-control s_website_form_input" name="material_description"/>').wrap(col).parent().appendTo(Row);
        $('<input type="number" class="form-control s_website_form_input" name="material_qty_request"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control s_website_form_input" name="material_serial_no"/>').wrap(col).parent().appendTo(Row);
        Row.appendTo($('.materials'));
    });

});