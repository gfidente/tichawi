$(document).ready(function() {
    $("img").addClass("img-thumbnail pull-right");
});

var csrftoken = $.cookie('csrftoken');

$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

function vote(post_url) {
    $.post(post_url, function(data) {
        if (data["res"] == "ERR" && data["error"] == "unauthenticated") {
            $('#login_dropdown').popover('show');
        } else if (data["res"] == "OK") {
            article_id = post_url.split('/')[2];
            disable_vote_action(article_id);
            increment_vote_counter(article_id);
        }
    });
}

function disable_vote_action(article_id) {
    selector = '#';
    selector = selector += article_id;
    selector = selector += '_vact';
    $(selector).addClass("disabled");
}

function increment_vote_counter(article_id) {
    selector = '#';
    selector = selector += article_id;
    selector = selector += '_vnum';
    cval = $(selector).text();
    nval = parseInt(cval) + 1;
    $(selector).text(nval);
}
