$(function() {
    $('#add-organization-button').on('click', function(e) {
        var field, fields, postData, field_names, i, len, admins;
        e.preventDefault();
        field_names = ['Organization Name', 'Description', 'Admins'];
        fields = [$('#input-title'), $('#input-description'), $('#input-admins')];
        for (i = 0, len = fields.length; i < len; i++) {
            field = fields[i];
            if (field.val().trim() === "") {
                alert('Missing: ' + field_names[i]);
                return;
            }
        }
        admins = fields[2].val().split(',');

        postData = {
            'title': fields[0].val().trim(),
            'description': fields[1].val().trim(),
            'admins': admins
        };
        return $.ajax({
            url: '/organizations',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function(data) {
                window.location.reload();
                if (data == 'Duplicate Organization') {
                    return alert('Duplicate Organization');
                }
                else {
                    return alert('Successfully added!');
                }
            }
        });
    });

    $('button[class="btn btn-danger deleteorganization"]').on('click', function() {
        var organization_id, tr;
        tr = $(this).parent().parent();
        organization_id = tr.attr('data-id');
        return $.ajax({
            url: '/organizations?id=' + organization_id,
            type: 'DELETE',
            success: function() {
                window.location.reload();
                return alert('Successfully deleted');
            }
        });
    });

});