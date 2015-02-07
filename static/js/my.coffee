jQuery ->
    $('button[class="close"]').click(deletePetition)

deletePetition = (e) ->
    petition = $(this).parent()
    petition_id = petition.attr('data-id')
    $.ajax
        url: '/petitions/delete'
        type: 'POST'
        data: 'id': petition_id
        success: (data) ->
            if data == 'Success!'
                petition.slideUp(500)