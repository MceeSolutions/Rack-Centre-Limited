odoo.define('rc_access_request.access_request', function(require){
    
    'use_strict';
    
    $('#add-more-attendees').click(function(e) {
        e.preventDefault();
        var Row = $("<div class='row'></div>");
        var col = $("<div class='form-group col-12 col-sm col-lg-3'></div>");
        $('<input type="text" class="form-control" name="visitor_name"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control" name="visitor_designation"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control" name="visitor_company"/>').wrap(col).parent().appendTo(Row);
        $('<input type="text" class="form-control" name="visitor_phone"/>').wrap(col).parent().appendTo(Row);
        Row.appendTo($('.attendees'));
    });

});
