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
                if (data == 'Duplicate Petition') {
                    return alert('Duplicate Petition');
                }
                window.location.reload();
            }
        });

    });

    $(document).on('click', 'button[class="btn btn-danger deletepetition"]', function(){
        var petition_id, tr;
        tr = $(this).parent().parent();
        petition_id = tr.attr('data-id');
        return $.ajax({
            url: '/my/delete',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function() {
                window.location.reload();
                return alert('Successfully deleted');
            }
        });
    });
    /*
    signPetition = function(e) {
        var petition, petition_id;
        console.log('Sign Petition Script ran!');
        petition = $(this).parent();
        petition_id = petition.attr('data-id');
        return $.ajax({
            url: '/petitions/sign',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function(data) {
                if (data === 'Successfully signed!') {
                    return alert('Signed successfully!');
                }
                if (data === 'You cannot sign your own petition!') {
                    return alert('You cannot sign your own petition!');
                }
            }
        });
    };

    unsignPetition = function(e) {
        var petition, petition_id;
        console.log('Unsign Petition Script ran!');
        petition = $(this).parent();
        petition_id = petition.attr('data-id');
        return $.ajax({
            url: '/petitions/unsign',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function(data) {
                if (data === 'Successfully unsigned!') {
                    return alert('Unsigned successfully!');
                }
                if (data === 'You cannot unsign your own petition!') {
                    return alert('You cannot unsign your own petition!');
                }
            }
        });
    };

    deletePetition = function(e) {
        var petition, petition_id;
        petition = $(this).parent();
        petition_id = petition.attr('data-id');
        return $.ajax({
            url: '/petitions/delete',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function(data) {
                if (data === 'Success!') {
                    return petition.slideUp(500);
                }
            }
        });
    };*/

}).call(this);