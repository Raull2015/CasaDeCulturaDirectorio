$(function(){
  $('#searchA').keyup(function(){
    $.ajax({
      type: 'POST',
      url: '/buscar/artista/',
      data: {
        'search_text': $('#searchA').val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: searchSuccess,
      dataType: 'html'
    });
  });

  $('#searchE').keyup(function(){
    $.ajax({
      type: 'POST',
      url: '/buscar/evento/',
      data: {
        'search_text': $('#searchE').val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: searchSuccess,
      dataType: 'html'
    });
  });
});

function searchSuccess(data, textStatus, jqXHR)
{
  $('#search-text').html(data);
}

function authorizeArtist(id) {
  var request = $.ajax({
    type: "POST",
    url: "/administracion/artista/",
    withCredentials:true,
    data: {
      "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
      "id": id
    },
  });
  request.done(function(data, textStatus, jqXHR) {
    $('#lista').html(data);
  });
}

function deleteArtist(id) {
  var request = $.ajax({
    type: "POST",
    url: "/administracion/artista/eliminar/",
    withCredentials:true,
    data: {
      "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
      "id": id
    },
  });
  request.done(function(response) {

  });
}

function authorizeEvent(id) {
  var request = $.ajax({
    type: "POST",
    url: "/administracion/evento/",
    withCredentials:true,
    data: {
      "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
      "id": id
    },
  });
  request.done(function(response) {

  });
}

function deleteEvent(id) {
  var request = $.ajax({
    type: "POST",
    url: "/administracion/evento/eliminar/",
    withCredentials:true,
    data: {
      "csrfmiddlewaretoken": $('input[name=csrfmiddlewaretoken]').val(),
      "id": id
    },
  });
  request.done(function(response) {

  });
}
