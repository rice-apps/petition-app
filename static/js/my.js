(function() {
    $('.positions').hide();

    $('#input-election').on('change', function(){
        $('.positions').hide();
        var election_id = $('#input-election').val();
        $('#' + election_id).show();
    });

    $('#add-petition-button').on('click', function() {
        var i, n, field, fields, postData, field_names, position;
        field_names = ['Name', 'Election'];
        fields = [$('#input-name'), $('#input-election')];
        for (i = 0, n = fields.length; i < n; i++) {
            field = fields[i];
            if (field.val().trim() === "") {
                alert('Missing: ' + field_names[i]);
                return;
            }
        }

        $('.positions').each(function() {
            if ($(this).val() != null)
                position = $(this).val();
        });

        if (!position) {
            alert('Missing: Position');
            return;
        }

        postData = {
            'name': fields[0].val(),
            'election': fields[1].val(),
            'position': position,
            'message': $('#input-message').val()
        };

        return $.ajax({
            url: '/my',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function(data) {
                window.location.reload();
                if (data == 'Duplicate Petition') {
                    return alert('Duplicate Petition');
                }
            }
        });

    });

    $(document).on('click', 'button[class="btn btn-danger deletepetition"]', function(){
        var petition_id, tr;
        tr = $(this).parent().parent();
        petition_id = tr.attr('data-id');
        return $.ajax({
            url: '/my?id=' + petition_id,
            type: 'DELETE',
            success: function() {
                window.location.reload();
                return alert('Successfully deleted');
            }
        });
    });

}).call(this);