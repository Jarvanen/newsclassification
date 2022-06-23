/*jshint jquery:true */
/*global $:true */

var $ = jQuery.noConflict();

$(document).ready(function($) {
  "use strict";

  /*-------------------------------------------------*/
  /* =  parallax
  /*-------------------------------------------------*/
  
  try{
    $('.parallax').appear(function() {
      $.stellar({
        horizontalScrolling: false,
        verticalOffset: 0,
        parallaxBackgrounds: true
      });
    });
    
  } catch(err) {
  }

    /*-------------------------------------------------*/
  /* =  portfolios
  /*-------------------------------------------------*/

  $('.portfolios-box').hover(
    function () {
      var overlay = $(this).find('.portfolios-box-overlay');
      overlay.removeClass(overlay.data('return')).addClass(overlay.data('hover'));

    },
    function () {
      var overlay = $(this).find('.portfolios-box-overlay');   
      overlay.removeClass(overlay.data('hover')).addClass(overlay.data('return'));
    }

  );

  /*-------------------------------------------------*/
  /* =  testimonials
  /*-------------------------------------------------*/
  
  $("#owl-quote").owlCarousel({
 
    items : 1, //10 items above 1000px browser width
    itemsDesktop : [1000,1], //5 items between 1000px and 901px
    itemsDesktopSmall : [900,1], // betweem 900px and 601px
    itemsTablet: [600,1], //2 items between 600 and 0
    itemsMobile : [300,1], // itemsMobile disabled - inherit from itemsTablet option
    transitionStyle : "backSlide",

    //Pagination
    pagination : true,
    paginationNumbers: false
 
  });

  /*-------------------------------------------------*/
  /* =  lightbox Image
  /*-------------------------------------------------*/

  $('.lightbox').magnificPopup({ 
  type: 'image'
  // other options
  });

  /*-------------------------------------------------*/
  /* =  Modal popup
  /*-------------------------------------------------*/

  $('.modal').magnificPopup({
      type: 'inline',
      preloader: false,
      focus: '#username',
      modal: true
    });

    $(document).on('click', '.popup-modal-dismiss', function (e) {
    e.preventDefault();
    $.magnificPopup.close();

  });

$('.gallery').each(function() { // the containers for all your galleries
    $(this).magnificPopup({
        delegate: 'a', // the selector for gallery item
        type: 'image',
        gallery: {
          enabled:true
        }
    });
}); 
 

  /*-------------------------------------------------*/
  /* =  Video and Map popup
  /*-------------------------------------------------*/
 
  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,

    fixedContentPos: false
  });

  /*-------------------------------------------------*/
  /* =  back to top
  /*-------------------------------------------------*/

  $('.backtotop').click(function(){
    $('html, body').animate({scrollTop:0}, 'slow');
  });

  /*-------------------------------------------------*/
  /* =  fix sidebar menu
  /*-------------------------------------------------*/

if (window.matchMedia('(min-width: 600px)').matches)
{
    // do functionality on screens smaller than 768px
    var offset = $(".canvas-menu-fix").offset();
    var topPadding = 0;

    $(window).scroll(function() {
    
        if ($(window).scrollTop() > offset.top) {
        
            $(".canvas-menu-fix").stop().animate({
            
                marginTop: $(window).scrollTop() - offset.top + topPadding
            
            });
        
        } else {
        
            $(".canvas-menu-fix").stop().animate({
            
                marginTop: 0
            
            });
        
        }
        
            
    });
}

  





});