$(document).ready(function(){
  console.log('ready!');

  var night = true;

  var nightTheme = "ace/theme/kr_theme";
  var dayTheme = "ace/theme/tomorrow"

  if ($("#editor").length){
    var editor = ace.edit("editor");
    editor.setTheme(nightTheme);
    editor.getSession().setMode("ace/mode/javascript");
    editor.setOptions({
        fontSize: "12px"
    });
    editor.container.style.lineHeight = 1.7

    var solution = ace.edit("solution");
    solution.setTheme(nightTheme);
    solution.getSession().setMode("ace/mode/javascript");
    solution.setOptions({
        fontSize: "12px"
    });
    solution.container.style.lineHeight = 1.7
  }

  $("#dayNight").click(function(){
    if (night) {
      if ($("#editor").length){
        editor.setTheme(dayTheme);
        solution.setTheme(dayTheme);
      }
      $("body").addClass("bodyDay");
      night = false;
      console.log(night);
    } else {
      if ($("#editor").length){
        editor.setTheme(nightTheme);
        solution.setTheme(nightTheme);
      }
      $("body").removeClass("bodyDay");
      night = true;
      console.log(night);
    }
  });

  $("#show_hide").click(function(){
    $("#solutions_div").toggle();
  })

  $("#testSubmit").click(function(){
    var value = editor.getValue();

    // from Django documentation
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    // replacement of Django documentation
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
          function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
              var cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
                }
              }
            }
            return cookieValue;
          }
          if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
        }
      }
    });

    $.ajax({
      type: "POST",
      url: "/calculate",
      data: {"input": value},
      success: function(data) {
        $("#testOutput").empty().html("Returned data is: " + data.input);
      },
      error: function(data) {
        $("#testOutput").empty().html("Error");
      }
    });

  });
});
