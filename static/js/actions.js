$(function () {
    "use strict";

    var appFactory = function () {
        var input = $('#poem'),
            response = $('#response'),
            button = $('#submit');
        var success = function (str) {
            console.log('here2');
            response.text(str);
            response.fadeIn(700);
        };
        return {
            init: function () {
                button.on('click', this.guess);
            },

            //Gets response decrypted based on value in the input box
            guess: function (e) {
                var str = input.val().replace(/\n/g, ' ');
                $.getJSON('/_classify/' + str, function (data) {
                    response.fadeOut(700, function () {
                        setTimeout(function () {
                            success(data.category);
                        }, 200);
                    });
                });
            }

        };
    };

    var app = appFactory();
    app.init();
});
