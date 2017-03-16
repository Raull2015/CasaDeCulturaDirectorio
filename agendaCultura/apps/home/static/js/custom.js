jQuery(document).ready(function(){

  //============================== MENU SCROLL =========================
   $(window).load(function(){
    $('.body-wrapper').each(function(){
      var header_area = $('.header-wrapper');
      var main_area = header_area.children('.navbar');

      var logo = main_area.find('.navbar-header');
      var navigation = main_area.find('.navbar-collapse');
      var original = {
        nav_top: navigation.css('margin-top')
      };

      $(window).scroll(function(){
        if( main_area.hasClass('bb-fixed-header') && ($(this).scrollTop() == 0 || $(this).width() < 750)){
          main_area.removeClass('bb-fixed-header').appendTo(header_area);
          navigation.animate({'margin-top': original.nav_top}, {duration: 300, queue: false, complete: function(){
            header_area.css('height', 'auto');
          }});
        }else if( !main_area.hasClass('bb-fixed-header') && $(this).width() > 750 &&
          $(this).scrollTop() > header_area.offset().top + header_area.height() - parseInt($('html').css('margin-top')) ){

          header_area.css('height', header_area.height());
          main_area.css({'opacity': '0'}).addClass('bb-fixed-header');
          main_area.appendTo($('body')).animate({'opacity': 1});

          navigation.css({'margin-top': '0px'});
        }
      });
    });

    $(window).trigger('resize');
    $(window).trigger('scroll');
  });

//============================== SELECT BOX =========================
  $('.select-drop').selectbox();

//============================== MENU DROPDOWN ON HOVER =========================
  $('.nav .dropdown').hover(function() {
    $(this).addClass('open');
  },
  function() {
    $(this).removeClass('open');
  }
  );

//============================== CART =========================
$('.cart-dropdown a').on("click",function() {
    $(".dropdown-menu").toggleClass('display-block');
    $(".cart-dropdown a i").toggleClass('fa-close').toggleClass("fa-shopping-basket");
    $(".badge").toggleClass('display-none');
});

//============================== Rs-Slider =========================
  jQuery('.bannercontainerV1 .fullscreenbanner').revolution({
   delay: 5000,
   startwidth: 1170,
   startheight: 560,
   fullWidth: "on",
   fullScreen: "off",
   hideCaptionAtLimit: "",
   dottedOverlay: "twoxtwo",
   navigationStyle: "preview4",
   fullScreenOffsetContainer: "",
   hideTimerBar:"on"
  });

  jQuery('.bannercontainerV3 .fullscreenbanner').revolution({
    delay: 5000,
    startwidth: 1170,
    startheight: 500,
    fullWidth: "on",
    fullScreen: "on",
    hideCaptionAtLimit: "",
     dottedOverlay: "twoxtwo",
    navigationStyle: "preview4",
    fullScreenOffsetContainer: "",
    hideTimerBar:"on",
  });

  jQuery('.bannercontainerV2 .fullscreenbanner').revolution({
   delay: 5000,
   startwidth: 1170,
   startheight: 660,
   fullWidth: "on",
   fullScreen: "off",
   hideCaptionAtLimit: "",
   dottedOverlay: "none",
   navigationStyle: "preview4",
   fullScreenOffsetContainer: "",
   hideTimerBar:"on"
  });
//============================== OWL-CAROUSEL =========================
  var owl = $('.owl-carousel.teamSlider');
  owl.owlCarousel({
    loop:true,
    margin:28,
    autoplay:false,
    autoplayTimeout:2000,
    autoplayHoverPause:true,
    nav:true,
    moveSlides: 4,
    dots: false,
    responsive:{
      320:{
        items:1
      },
      768:{
        items:3
      },
      992:{
        items:4
      }
    }
  });

  var owl = $('.owl-carousel.commentSlider');
  owl.owlCarousel({
    loop:true,
    margin:28,
    autoplay:false,
    autoplayTimeout:3000,
    autoplayHoverPause:true,
    nav:true,
    moveSlides: 1,
    dots: false,
    responsive:{
      320:{
        items:1
      },
      768:{
        items:1
      },
      992:{
        items:1
      }
    }
  });

  var owl = $('.owl-carousel.partnersLogoSlider');
    owl.owlCarousel({
      loop:true,
      margin:28,
      autoplay:true,
      autoplayTimeout:2000,
      autoplayHoverPause:true,
      nav:true,
      dots: false,
      responsive:{
        320:{
          slideBy: 1,
          items:1
        },
        768:{
          slideBy: 1,
          items:3
        },
        992:{
          slideBy: 1,
          items:5
        }
      }
    });
//============================== COUNTER-UP =========================
  $(document).ready(function ($) {
    $('.counter').counterUp({
      delay: 10,
      time: 2000
    });
  });

  //============================== BACK TO TOP =========================
    $(document).ready(function(){
      $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
          $('#backToTop').css("opacity", 1);
        } else {
          $('#backToTop').css("opacity", 0);
        }
      });
    });

  //============================== SMOOTH SCROLLING TO SECTION =========================
  $(document).ready(function () {
    $('.scrolling  a[href*="#"]').on('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var target = $(this).attr('href');
      $(target).velocity('scroll', {
        duration: 800,
        offset: -150,
        easing: 'easeOutExpo',
        mobileHA: false
      });
    });
  });

//============================== PRICE SLIDER RANGER =========================
var minimum = 20;
var maximum = 300;

$( "#price-range" ).slider({
  range: true,
  min: minimum,
  max: maximum,
  values: [ minimum, maximum ],
  slide: function( event, ui ) {
    $( "#price-amount-1" ).val( "$" + ui.values[ 0 ] );
    $( "#price-amount-2" ).val( "$" + ui.values[ 1 ] );
  }
});

$( "#price-amount-1" ).val( "$" + $( "#price-range" ).slider( "values", 0 ));
$( "#price-amount-2" ).val( "$" + $( "#price-range" ).slider( "values", 1 ));

//============================== ACCORDION OR COLLAPSE ICON CHANGE =========================

    var allIcons = $("#faqAccordion .panel-heading i.fa");
    $('#faqAccordion .panel-heading').click(function(){
      allIcons.removeClass('fa-chevron-down').addClass('fa-chevron-up');
      $(this).find('i.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });

    var allIconsOne = $("#accordionOne .panel-heading i.fa");
    $('#accordionOne .panel-heading').click(function(){
      allIconsOne.removeClass('fa-chevron-down').addClass('fa-chevron-up');
      $(this).find('i.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });

    var allIconsTwo = $("#accordionTwo .panel-heading i.fa");
    $('#accordionTwo .panel-heading').click(function(){
      allIconsTwo.removeClass('fa-chevron-down').addClass('fa-chevron-up');
      $(this).find('i.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });

    var allIconsThree = $("#togglesOne .panel-heading i.fa");
    $('#togglesOne .panel-heading').click(function(){
      allIconsThree.removeClass('fa-chevron-down').addClass('fa-chevron-up');
      $(this).find('i.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });

    var allIconsFour = $("#togglesTwo .panel-heading i.fa");
    $('#togglesTwo .panel-heading').click(function(){
      allIconsFour.removeClass('fa-chevron-down').addClass('fa-chevron-up');
      $(this).find('i.fa').removeClass('fa-chevron-up').addClass('fa-chevron-down');
    });

  //============================== Product Gallery =========================
  var galleryThumb = $('.product-gallery-thumblist a'),
      galleryPreview = $('.product-gallery-preview > li');


  galleryThumb.on('click', function(e) {
    var target = $(this).attr('href');

    galleryThumb.parent().removeClass('active');
    $(this).parent().addClass('active');
    galleryPreview.removeClass('current');
    $(target).addClass('current');

    e.preventDefault();
  });

  // Count Input (Quantity)
  //------------------------------------------------------------------------------
  $(".incr-btn").on("click", function(e) {
    var $button = $(this);
    var oldValue = $button.parent().find('.quantity').val();
    $button.parent().find('.incr-btn[data-action="decrease"]').removeClass('inactive');
    if ($button.data('action') == "increase") {
      var newVal = parseFloat(oldValue) + 1;
    } else {
     // Don't allow decrementing below 1
      if (oldValue > 1) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 1;
        $button.addClass('inactive');
      }
    }
    $button.parent().find('.quantity').val(newVal);
    e.preventDefault();
  });


});


  $(function() {
      // This function gets cookie with a given name
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

      /*
      The functions below will create a header with csrftoken
      */

      function csrfSafeMethod(method) {
          // these HTTP methods do not require CSRF protection
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      }
      function sameOrigin(url) {
          // test that a given url is a same-origin URL
          // url could be relative or scheme relative or absolute
          var host = document.location.host; // host + port
          var protocol = document.location.protocol;
          var sr_origin = '//' + host;
          var origin = protocol + sr_origin;
          // Allow absolute or scheme relative URLs to same origin
          return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
              (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
              // or any other URL that isn't scheme relative or absolute i.e relative.
              !(/^(\/\/|http:|https:).*/.test(url));
      }

      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                  // Send the token to same-origin, relative URLs only.
                  // Send the token only if the method warrants CSRF protection
                  // Using the CSRFToken value acquired earlier
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

  });

  function logear() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/login/", // the endpoint
        type : "POST", // http method
        data : { username : $('#id_username').val() ,
                 password : $('#id_password').val()}, // data sent with the post request
        // handle a successful response
        success : function(json) {
          //  $('#id_username').val('');
          //  $('#id_password').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json['autorizado'] == false){
                $('#results').html("<p class='help-block'><a href='#'>Tu usuario no ha sido autorizado</a></p>");
            }
            else {
              var next = getParameterByName("next")
              console.log(next)
              if (next != ""){
                window.location = next;
              }
              else{
                window.location="/home/";
              }
            }

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<p class='help-block'><a href='#'>Usuario o Contraseña Incorrecto</a></p>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  };

  function crear_usuario() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/home/registro/", // the endpoint
        type : "POST", // http method
        data : { usuario : $('#id_usuario').val(),
                 contrasenia : $('#id_contrasenia').val(),
                 r_contrasenia : $('#id_contrasenia_r').val(),
                 nombre : $('#id_nombre').val(),
                 email : $('#id_email').val(),
                 telefono : $('#id_telefono').val(),
                 nacimiento : $('#id_nacimiento').val(),
                 sexo : $('#id_genero').val() }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            $('#id_usuario').val('');
          //  $('#id_password').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json['existe'] == true){
                if(json['error'] == true){
                  $('#results_2').html("<p class='help-block'><a href='#'>" + json['mensaje'] + "</a></p>");
                }
                else{
                  $('#results_2').html("<p class='help-block'><a href='#'>Ya existe el nombre de usuario</a></p>");
                }
            }
            else {
                window.location="/home/confirmar_registro/";
            }

        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results_2').html("<p class='help-block'><a href='#'>Ocurrio un error</a></p>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  };

  /*function editar_perfil(formData) {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : window.location.href, // the endpoint
        type : "POST", // http method
        data : formData, // data sent with the post request
        // handle a successful response
        success : function(json) {
          // $('#id_usuario').val('');
          // $('#id_password').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check

            $('#results_2').html("<p class='help-block'><a href='#'>Tu perfil ha sido actualizado</a></p>");

              window.location = json['redirect'];
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results_2').html("<p class='help-block'><a href='#'>Ocurrio un error</a></p>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  };*/

  /*function crear_evento() {
    console.log("create post is working!")
    $.ajax({
      url : 'home/crear_evento/',
      type : 'POST',
      data : {
        nombre : $('#nombre').val().
        lugar : $('#lugar').val(),
        fecha : $('#fecha').val(),
        hora : $('#hora').val(),
        descripcion : $('#descripcion').val(),
        imagen : $('#imagen').val(),
        categoria : $('#categoria').val()
      },
      success : function() {
        console.log("success");
      },
      error : function(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
      }
    });
  };*/

  $('#post-login').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    logear();
  });

  $('#post-crear-user').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    crear_usuario();
  });

  $('#crearEvento').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!");  // sanity check
    crear_evento();
  });

  /*$('#editar_evento').on('submit', function(event){
    event.preventDefault();
    var f = $(this);
    var formData = new FormData(document.getElementById("editarPerfil"));
    editar_perfil(formData);
  });*/

  $('#cambiarContrasenia').on('submit', function(event){
    event.preventDefault();
    var f = $(this);
    var formData = new FormData(document.getElementById("cambiarContrasenia"));
    cambiar_contrasenia(formData);
  });

  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }
