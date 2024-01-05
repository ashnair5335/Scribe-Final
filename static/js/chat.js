function sendMessage() {
    var user_input = $('#user-input').val();
    $('#chat-box').append('<p class="user-message">User: ' + user_input + '</p>');

    $.ajax({
        type: 'POST',
        url: '/chat',
        data: {user_input: user_input},
        success: function(data) {
            var response = data.response;
            $('#chat-box').append('<p class="server-message">Scribe: ' + response + '</p>');
            $('#user-input').val('');
            $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
        }
    });
}


$('#user-input').on('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    });

$('#user-input').keypress(function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

$('#user-input').keypress(function(e) {
    if (e.which === 13 && e.shiftKey) {
        var content = this.value;
        var caret = this.selectionStart;
        this.value = content.substring(0, caret) + '\n' + content.substring(this.selectionEnd);
        this.selectionStart = this.selectionEnd = caret + 1;
        e.preventDefault();
    }
});