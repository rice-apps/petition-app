// Generated by CoffeeScript 1.8.0
(function() {
  var deletePetition, unsignPetition, signPetition;

  jQuery(function() {
    console.log('Petition script ran!');
    $('#add-button').click((function(_this) {
      return function(e) {
        var field, fields, postData, _i, _len, field_names;
        e.preventDefault();
        field_names = ['Candidate Name', 'Candidate Email', 'Election', 'Organization Name', 'Position Name', 'Message(optional)']
        fields = [$('#input-name'), $('#input-email'), $('#input-election'), $('#input-organization'), $('#input-position'), $('#input-text')];
        for (_i = 0, _len = fields.length; _i < _len; _i++) {
          field = fields[_i];
          if (field.val().trim() === "" && field_names[_i] != 'Message(optional)') {
            alert('Missing: ' + field_names[_i]);
            return;
          }
        }
        
        if (checkEmail($('#input-email').val()) == false) {
          alert('Invalid Email');
          return
        }
        
        postData = {
          'name': fields[0].val(),
          'email': fields[1].val(),
          'election': fields[2].val(),
          'organization': fields[3].val(),
          'position': fields[4].val(),
          'message': fields[5].val()
        };
        return $.ajax({
          url: '/petitions',
          type: 'POST',
          data: {
            'data': JSON.stringify(postData)
          },
          success: function(data) {
            var html, response;
            response = JSON.parse(data);
            
            if (response['id'] == 'Duplicate Petition') {
              return alert('Duplicate Petition');
            }
            else {
							var election = response['election'].split('-')[0];
							election = election.substring(0, election.length - 1);
							
              html = $("<div class='alert' data-id='" + response['id'] + "'> <button type='button' class='close deletePetition' data-dismiss='alert'>"
							+ "&times;</button> <h4><b>" + response['name'] + " </b>is running for " + response['organization'] + ": " + response['position'] +
							"</h4> <h5>Election: " + election + "</h5> <h6>Number of Signatures: 0</h6> <p>" + response['message'] +
							"</p> <button type='button' id='ign-button' class='btn btn-mini'>Sign</button> <button type='button' id='unsign-button'" 
							+ "class='btn btn-mini'>Unsign</button> </div>");

              $('#petitions').prepend(html);
            
              html.hide().slideDown(500);
              return html.children('button[class="close deletePetition"]').click(deletePetition);
            }
            
          }
        });
      };
    })(this));
    $('button[class="close deletePetition"]').click(deletePetition);
    $('button[id="sign-button"]').click(signPetition);
    return $('#unsign-button').click(unsignPetition);
  });

  signPetition = function(e) {
    var petition, petition_id;
    console.log('Script ran!');
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
    console.log('Script ran!');
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
  };

}).call(this);

function checkEmail(emailAddress) {
  var sQtext = '[^\\x0d\\x22\\x5c\\x80-\\xff]';
  var sDtext = '[^\\x0d\\x5b-\\x5d\\x80-\\xff]';
  var sAtom = '[^\\x00-\\x20\\x22\\x28\\x29\\x2c\\x2e\\x3a-\\x3c\\x3e\\x40\\x5b-\\x5d\\x7f-\\xff]+';
  var sQuotedPair = '\\x5c[\\x00-\\x7f]';
  var sDomainLiteral = '\\x5b(' + sDtext + '|' + sQuotedPair + ')*\\x5d';
  var sQuotedString = '\\x22(' + sQtext + '|' + sQuotedPair + ')*\\x22';
  var sDomain_ref = sAtom;
  var sSubDomain = '(' + sDomain_ref + '|' + sDomainLiteral + ')';
  var sWord = '(' + sAtom + '|' + sQuotedString + ')';
  var sDomain = sSubDomain + '(\\x2e' + sSubDomain + ')*';
  var sLocalPart = sWord + '(\\x2e' + sWord + ')*';
  var sAddrSpec = sLocalPart + '\\x40' + sDomain; // complete RFC822 email address spec
  var sValidEmail = '^' + sAddrSpec + '$'; // as whole string

  var reValidEmail = new RegExp(sValidEmail);

  return reValidEmail.test(emailAddress);
}