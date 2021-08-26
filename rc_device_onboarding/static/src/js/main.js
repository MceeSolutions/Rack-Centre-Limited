odoo.define('rc_device_onboarding.device_onboarding', function(require){
    
    'use_strict';
    
    $('#add-onboarding-equipments').click(function(e) {
        e.preventDefault();
        var Row = $("<div class='row'></div>");
        var col = $("<div class='form-group s_website_form_field col-12 s_website_form_required col-lg-2' data-type='char' data-name='Field'></div>");
        $('<input type="text" class="form-control s_website_form_input" name="equipment_manufacturer"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control s_website_form_input" name="equipment_model"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control s_website_form_input" name="equipment_serial_numbers"/>').wrap(col).parent().appendTo(Row);
        $('<select class="form-control o_website_form_input" name="equipment_power_requirements" id="equipment_power_requirements"><option value="ac_single_phase">AC: Single Phase</option><option value="three_phase">Three Phase</option><option value="dc_voltage">DC: Voltage</option></select>').wrap(col).parent().appendTo(Row);
        // $('<input type="text" class="form-control s_website_form_input" name="equipment_power"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control s_website_form_input" name="equipment_u_space"/>').wrap(col).parent().appendTo(Row);
        $('<select class="form-control o_website_form_input" name="equipment_power_requirements" id="equipment_power_requirements"><option value="single">Single</option><option value="dual">Dual</option></select>').wrap(col).parent().appendTo(Row);
        Row.appendTo($('.equipments'));
    });

});