$(document).ready(function(){
  console.log('ready!');

  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/mono_industrial");
  editor.getSession().setMode("ace/mode/javascript");

  var solution = ace.edit("solution");
  solution.setTheme("ace/theme/mono_industrial");
  solution.getSession().setMode("ace/mode/javascript");

  $("#show_hide").click(function(){
    $("#solutions_div").toggle();
  })



  $("#testSubmit").click(function(){
    // var editor = ace.edit("editor")
    var value = editor.getValue();
    // $("#testOutput").empty().html(value);

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

    var csrf_token = $('meta[name="csrf-token"]').attr('content');

    // var data = {
    //   'value': value,
    //   'X-CSRFToken': csrftoken
    // }
    // console.log(data);


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
      data: {"value": value},
      success: function(data) {
        console.log("data",data);
        $("#testOutput").empty().html("Returned data is:",data);
      },
      error: function(data) {
        $("#testOutput").empty().html("Error");
      }
    });

    // $.post("/calculate", { 'value': value, 'csrfmiddlewaretoken': '{{ csrf_token }}' }, function(data) {
    //   $("#testOutput").empty().html("Returned data:",data);
    // });

  });
});
