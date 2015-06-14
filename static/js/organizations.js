(function() {
  var deleteOrganization;

  jQuery(function() {
    console.log('Organization script ran!');
    $('#add-organization-button').click((function(_this) {
      return function(e) {
        var field, fields, postData, _i, _len, field_names;
        e.preventDefault();
        field_names = ['Organization Name', 'Description', 'Admins'];
        fields = [$('#input-title'), $('#input-description'), $('#input-admins')];
        for (_i = 0, _len = fields.length; _i < _len; _i++) {
          field = fields[_i];
          if (field.val().trim() === "") {
            alert('Missing: ' + field_names[_i]);
            return;
          }
        }
        
        postData = {
          'title': fields[0].val(),
          'description': fields[1].val(),
          'admins': fields[2].val()
        };
        return $.ajax({
          url: '/organizations',
          type: 'POST',
          data: {
            'data': JSON.stringify(postData)
          },
          success: function(data) {
            var html, response, htmlstr;
            response = JSON.parse(data);
            if (response['id'] == 'Duplicate Organization') {
              return alert('Duplicate Organization');
            }
            else {
                htmlstr = "<tr data-id = '" + response['id'] + "'><td>" + response['title'] + "</td><td>" + response['description'] +
                    "<td><button type='button' class='btn btn-default'>Dashboard</button></td>";
                if (response['netid'] == 'rsk8') {
                    htmlstr = htmlstr + "<td><button type='button' class='btn btn-default deleteorganization'>Delete</button></td></tr>";
                }
                else {
                    htmlstr = htmlstr + "<td></td></tr>";
                }
              html = $(htmlstr);
              
              $('#organizations').append(html);

              return html.children('button[class="btn btn-default deleteorganization"]').click(deleteOrganization);
            }
          }
        });
      };
    })(this));
    $('button[class="btn btn-default deleteorganization"]').click(deleteOrganization);
  });

  deleteOrganization = function(e) {
      var organization_id, tr;
      tr = $(this).parent().parent();
      organization_id = tr.attr('data-id');
      return $.ajax({
          url: '/organizations/delete',
          type: 'POST',
          data: {
              'id': organization_id
      },
      success: function(data) {
          console.log(tr);
          tr.remove();
          return alert('Successfully deleted');
      }
    });
  };

}).call(this);