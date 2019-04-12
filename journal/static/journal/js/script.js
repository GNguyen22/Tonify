$(document).ready(function() {
   $.fn.modal.Constructor.prototype.enforceFocus = function () {};
    $("#login-submit").on("submit", function(e) {
      //console.log("this is the right js file");
      e.preventDefault();
      url = location.protocol + "//" + location.host + "/journal/storeUser"
      var userNameArea = $('input#userNameInput');
      var userName = userNameArea.val();
      var genreArea = $('input#genreInput');
      var genre = genreArea.val();
      localStorage.setItem('userName', userName);
      console.log(userName);
      $.ajax({
            type: "POST",
            url: url,
            data: {
                "input": userName,
            },
            statusCode: {
                500: function() {
                    $("#returned").empty();
                    $("<p>Oops, looks like there's a database error!</p>").appendTo("#returned");
                }
            },
            beforeSend: function(xhr) {
                userNameArea.val('');
                $("#returned").empty();
                //$("<p>loading...</p>").appendTo("#returned");
                $("#login-menu-button").text(userName);
                //$("#exampleModal").modal('hide');
                //$('.modal-backdrop').removeClass('show');
            var $currentModals = $('.modal.in');
            console.log($currentModals);
            if ($currentModals.length > 0) { // if we have active modals
               console.log('here1');
               $currentModals.one('hidden.bs.modal', function () {
                  console.log('here2');
                     //$('.modal-backdrop').removeClass('show');
                     window.setTimeout(function(){
                     // when they've finished hiding
                     $('#selectGenreModal').modal('show');
                     $('#selectGenreModal').addClass('show');
                     $(document).off('focusin.modal');
                  }, 500);
               }).modal('hide');
            } else {
               $('selectGenreModal').modal('show');
               $('#selectGenreModal').addClass('show');
               $(document).off('focusin.modal');

            }               
                console.log(userName);
            }

        })
    });

    $("#genre-submit").on("submit", function(e) {
        e.preventDefault();

        url = location.protocol + "//" + location.host + "/journal/storeGenre"
      var genre = $('#genreInput :selected').text();
      //var genre = genreArea.val();
      var userName = localStorage.getItem('userName');
      console.log(genre);
      $.ajax({
            type: "POST",
            url: url,
            data: {
                "input": genre,
                "userName": userName,
            },
            statusCode: {
                500: function() {
                    $("#returned").empty();
                    $("<p>Oops, looks like there's a database error!</p>").appendTo("#returned");
                }
            },
            beforeSend: function(xhr) {
                //genreArea.val('');
                $("#returned").empty();
                $("#selectGenreModal").modal('hide');
                $('.modal-backdrop').removeClass('show');
                $('.modal').removeClass('show')
                $('div').remove('.modal-backdrop')
               console.log(genre);
            }

        })
    });


    $("#form-submit").on("submit", function(e) {
        e.preventDefault();

        url = location.protocol + "//" + location.host + "/journal/returnPlaylist"

        var textarea = $('textarea#taskInput');
        var text = textarea.val();

      var userName = localStorage.getItem('userName');
       console.log(text);
        $.ajax({
            type: "POST",
            url: url,
            data: {
                "input": text,
                "userName": userName,
            },
            statusCode: {
                500: function() {
                    $("#returned").empty();
                    $("<p>Oops, looks like there's a server error!</p>").appendTo("#returned");
                }
            },
            beforeSend: function(xhr) {
                textarea.val('');
                $("#returned").empty();
                //$("<p>loading...</p>").appendTo("#returned");
                //$("button").text("Loading...");
                console.log(text);
            }

        }).done(function(data) {
            $("#returned").empty();
            //$("button").text("Generate Playlist");
            var songs = data.tracks;
            console.log(songs);
            for (var i = 0; i < songs.length; i++) {
                /*
                var div =
                "<div class='container-fluid'> \
                    <div class='col-md-6'> \
                        <a href=" + songs[i].external_urls.spotify + "> \
                            <img src=" + songs[i].album.images[0].url + " class='img-responsive'/> \
                        </a> \
                    </div> \
                    <div class='col-md-6'> \
                        <h3>Song: " + songs[i].name + "</h3> \
                        <h3>Artist: " + songs[i].album.artists[0].name + "</h3> \
                        <h3>Album: " + songs[i].album.name + "</h3> \
                    </div> \
                </div>"
                */
                var div =
                "<div class='col-md-3'> \
                    <a href=" + songs[i].external_urls.spotify + "> \
                        <img src=" + songs[i].album.images[0].url + " class='img-responsive'/> \
                    </a> \
                    <h6>Song: " + songs[i].name + "</h6> \
                    <h6>Artist: " + songs[i].album.artists[0].name + "</h6> \
                    <h6>Album: " + songs[i].album.name + "</h6> \
                </div>";
                console.log(div);
                $(div).appendTo("#returned");
            }

            //$("<p>" + data["queryResult"]["fulfillmentText"] + "</p>").appendTo("#returned");
        });
    });
});
