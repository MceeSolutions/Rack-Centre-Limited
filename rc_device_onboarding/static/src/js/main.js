odoo.define('rc_device_onboarding.device_onboarding', function(require){
    
    'use_strict';
    
    $('#add-more-equipments').click(function(e) {
        e.preventDefault();
        var Row = $("<div class='row'></div>");
        var col = $("<div class='form-group s_website_form_field col-12 s_website_form_required col-lg-3' data-type='char' data-name='Field'></div>");
        $('<input type="text" class="form-control s_website_form_input" name="task_name"/>').wrap(col).parent().appendTo(Row);
        $('<input type="datetime-local" class="form-control s_website_form_input" name="task_start_date"/>').wrap(col).parent().appendTo(Row);
        $('<input type="datetime-local" class="form-control s_website_form_input" name="task_end_date"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control s_website_form_input" name="task_assigned_resource"/>').wrap(col).parent().appendTo(Row);
        Row.appendTo($('.equipments'));
    });

});