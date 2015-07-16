$(function() {
    $('#add-positions-row').on('click', function() {
        var htmlstr = '<tr><td><input class="form-control input-position" type="text"></td></tr>';
        $('#input-positions-table').append(htmlstr);
    });

    $('#delete-positions-row').on('click', function() {
        $('#input-positions-table tr:last').remove();
    });

    $('#add-admins-row').on('click', function() {
        var htmlstr = '<tr><td><input class="form-control input-positions"></td></tr>';
        $('#admins-table').append(htmlstr);
    });

    $('#delete-admins-row').on('click', function() {
        var last_row, form_control;

        last_row = $('#admins-table tr:last');
        form_control = last_row.children().children();
        if (!form_control[0].readOnly) {
            last_row.remove()
        }
    });

    $('#save-admins').on('click', function() {
        var fields, i, n, postData;
        //Get all the fields
        fields = [];
        for (i=0, n=$('.input-admin').length; i<n; i++) {
            if ($('.input-admin')[i].value.trim() != '') {
                fields[fields.length] = $('.input-admin')[i].value.trim();
            }
        }
        postData = {
                'admins': fields,
                'organization_id': $('#organization-data').data('id')
        };
        return $.ajax({
            url: '/dashboard/admins',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function() {
                window.location.reload();
                alert('Successfully saved changes to admins!')
            }
        });
    });

    $('#submit-election-button').on('click', function(e) {
        var field, fields, field_names, i, n;
        e.preventDefault();
        field_names = ['Election Name', 'Start Date', 'End Date'];
        fields = [$('#input-title'), $('#input-start-date'), $('#input-end-date')];
        for (i = 0, n = fields.length; i < n; i++) {
            field = fields[i];
            if (field.val().trim() === "") {
                alert('Missing: ' + field_names[i]);
                return;
            }
        }

        //Check dates validity
        var start, start_date, end, end_date, today;
        start = fields[1].val().split('-');
        start_date = new Date(Number(start[0]),Number(start[1]) -1 ,Number(start[2]));
        end = fields[2].val().split('-');
        end_date = new Date(Number(end[0]),Number(end[1]) -1 ,Number(end[2]));
        today = new Date();

        if (start_date >= end_date) {
            alert('End date must be later than start date');
            return;
        }
        if (start_date <= today || end_date <= today) {
            alert('Start and End Dates must be later than today');
            return;
        }

        //Get all the submitted positions
        var positions = [];
        for (i=0, n=$('.input-position').length; i<n; i++) {
            if ($('.input-position')[i].value.trim() != '') {
                positions[positions.length] = $('.input-position')[i].value.trim();
            }
        }

        var postData = {
            'title': fields[0].val().trim(),
            'start_date': fields[1].val().trim(),
            'end_date': fields[2].val().trim(),
            'positions': positions,
            'organization_id': $('#organization-data').data('id')
        };
        return $.ajax({
            url: '/dashboard/elections',
            type: 'POST',
            data: {
                'data': JSON.stringify(postData)
            },
            success: function(data) {
                window.location.reload();
                if (data == 'Duplicate Election') {
                    return alert('Duplicate Election');
                }
            }
        });
    });

    $('button[class="btn btn-danger deleteelection"]').on('click', function() {
        var election_id, tr;
        tr = $(this).parent().parent();
        election_id = tr.attr('data-id');
        return $.ajax({
            url: '/dashboard/elections?id=' + election_id,
            type: 'DELETE',
            success: function() {
                window.location.reload();
                return alert('Successfully deleted');
            }
        });
    });
});