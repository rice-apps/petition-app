$(function() {

    $(document).on('click', 'button[class="btn btn-info signpetition"]', function(){
        var petition_id, tr;
        tr = $(this).parent().parent();
        petition_id = tr.attr('data-id');
        return $.ajax({
            url: '/petitions/sign',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function(data) {
                window.location.reload();
                if (data === 'Successfully signed!') {
                    return alert('Signed successfully!');
                }
                if (data === 'You cannot sign your own petition!') {
                    return alert('You cannot sign your own petition!');
                }

            }
        });
    });

    $(document).on('click', 'button[class="btn btn-success unsignpetition"]', function(){
        var petition_id, tr;
        tr = $(this).parent().parent();
        petition_id = tr.attr('data-id');
        return $.ajax({
            url: '/petitions/unsign',
            type: 'POST',
            data: {
                'id': petition_id
            },
            success: function(data) {
                window.location.reload();
                if (data === 'Successfully unsigned!') {
                    return alert('Unsigned successfully!');
                }
                if (data === 'You cannot unsign your own petition!') {
                    return alert('You cannot unsign your own petition!');
                }

            }
        });
    });

});
