box.cfg{
    listen=3305
}

box.schema.user.grant('guest', 'read', 'universe', nil, {if_not_exists=true})

box.once("quest", function()
    box.schema.sequence.create('message_S')
    box.schema.space.create('message', {
        if_not_exists = true,
        format={
             {name = 'id', type = 'unsigned'},
             {name = 'quest_id', type = 'unsigned'},
             {name = 'type', type = 'string'},
             {name = 'text', type = 'string'},
             {name = 'buttons', type = 'array'}
        }
    })
    box.space.message:create_index('id', {
        sequence = 'message_S',
        parts = {'id'}
    })    
    box.space.message:create_index('quest_id', {
        parts = {'quest_id'},
        if_not_exists = true,
        unique = false
    })
    box.schema.sequence.create('quest_S')
    box.schema.space.create('quest_button', {
        if_not_exists = true,
        format={
             {name = 'id', type = 'unsigned'},
             {name = 'is_public', type = 'boolean'},
             {name = 'text', type = 'string'},
             {name = 'callbackData', type = 'string'}
        }
    })
    box.space.quest_button:create_index('id', {
        sequence = 'quest_S',
        parts = {'id'}
    })
    box.schema.space.create('user', {
        if_not_exists = true,
        format={
            {name = 'user_id', type = 'string'},
            {name = 'quest_id', type = 'unsigned'},
            {name = 'message_id', type = 'unsigned'},
            {name = 'end_id_send_message', type = 'unsigned'},
            {name = 'type_action', type = 'string'},
            {name = 'is_admin', type = 'boolean'},
            {name = 'hash_string', type = 'string'},
            {name = 'history', type = 'map'}
        }
    })
    box.space.user:create_index('id', {
        type = 'hash',
        parts = {'user_id'},
        if_not_exists = true,
        unique = true
    })           
end
)
