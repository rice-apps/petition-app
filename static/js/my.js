$(function() {
    $('#input-election').on('change', function(){
        var election_id = $('#input-election').val();
        return $.ajax({
            url: '/my/positions',
            type: 'POST',
            data: {
                'id': election_id
            },
            success: function(data) {
                var response, htmlstr, i;
                response = JSON.parse(data);
                htmlstr = '<option value="Select a Position" disabled selected>--Select a Position--</option>';
                for (i = 0; i < response.length; i++) {
                    htmlstr += '<option value="' + response[i] + '">' + response[i] + '</option>';
                }
                $("select[name='input-position']").find('option').remove().end().append($(htmlstr));
            }
        });
    });

    $('#add-petition-button').on('click', function() {
        var i, n, field, fields, postData, field_names;
        field_names = ['Name', 'Election', 'Position', 'Message'];
        fields = [$('#input-name'), $('#input-election'), $('#input-position'), $('#input-message')];
        for (i = 0, n = fields.length; i < n; i++) {
            field = fields[i];
            if (field.val().trim() === "" && field_names[i] != 'Message') {
                alert('Missing: ' + field_names[i]);
                return;
            }
        }

        postData = {
            'name': fields[0].val(),
            'election': fields[1].val(),
            'position': fields[2].val(),
            'message': fields[3].val()
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

});