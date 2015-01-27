jQuery ->
    console.log('Script ran')
    $('#add-button').click (e) =>
        e.preventDefault()
        fields = [$('#input-title'), $('#input-text')]
        for field in fields
            if field.val().trim() == ""
                alert('Missing input')
                return

        postData =
            'title': fields[0].val()
            'note': fields[1].val()

        $.ajax
            url: '/petitions'
            type: 'POST'
            data: 'data': JSON.stringify(postData)
            success: (data) ->
                response = JSON.parse(data)
                id = response['id']
                title = response['title']
                note = response['note']
                html = $("
                    <div class='alert' data-id='#{id}'>
                    <button type='button' class='close' data-dismiss='alert'>&times;</button>
                    <h4>#{title}</h4>
                    <h6>0</h6>
                    <p>#{note}</p>
                    <button type='button' id='vote-button' class='btn btn-mini'>Vote</button>
                    </div>")
                $('#petitions').prepend(html)
                html.hide().slideDown(500)
                html.children('button[class="close"]').click(deletePetition)

    $('button[class="close"]').click(deletePetition)
    $('#vote-button').click(votePetition)
    $('#unvote-button').click(unvotePetition)
    
votePetition = (e) ->
    console.log('Script ran!')
    petition = $(this).parent()
    petition_id = petition.attr('data-id')
    $.ajax
        url: '/petitions/vote'
        type: 'POST'
        data: 'id': petition_id
        success: (data) ->
            if data == 'Successfully voted!'
                alert('Voted successfully!')

unvotePetition = (e) ->
    console.log('Script ran!')
    petition = $(this).parent()
    petition_id = petition.attr('data-id')
    $.ajax
        url: '/petitions/unvote'
        type: 'POST'
        data: 'id': petition_id
        success: (data) ->
            if data == 'Successfully unvoted!'
                alert('Unvoted successfully!')

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