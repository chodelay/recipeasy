$(document).ready(function() {
  hideElement = function(elementID) {
    $('#' + elementID).toggle();
  }

  $('.item-text').on('click', function(e) {
    $(this).toggleClass('item-marked');
    e.preventDefault();
  });

  $('li').on('click', function(e) {
    $(this).toggleClass('step-marked');
    e.preventDefault();
    var isAllMarked = 1;
    var isOneUnmarked = 0;
    $(this).parent().find('li').each(function () {
      if (!$(this).hasClass('step-marked')) {
        isAllMarked = 0;
      }
    });
    if (isAllMarked === 1) {
      $(this).parent().parent().find('h3').addClass('step-marked');
      $(this).parent().parent().find('.timer_active').addClass('step-marked');
      $(this).parent().parent().find('.timer_inactive').addClass('step-marked');
    } else {
      $(this).parent().parent().find('h3').removeClass('step-marked');
      $(this).parent().parent().find('.timer_active').removeClass('step-marked');
      $(this).parent().parent().find('.timer_inactive').removeClass('step-marked');
    }
  });

  $('h3').on('click', function(e) {
    if ($(this).hasClass('step-header')) {
      if ($(this).hasClass("step-marked")) {
        $(this).parent().find('ul>li').removeClass('step-marked');
        $(this).parent().find('.row>.timer_active').removeClass('step-marked');
        $(this).parent().find('.row>.timer_inactive').removeClass('step-marked');
        $(this).removeClass('step-marked');
      } else {
        console.log("step-header");
        $(this).parent().find('ul>li').addClass('step-marked');
        $(this).parent().find('.row>.timer_active').addClass('step-marked');
        $(this).parent().find('.row>.timer_inactive').addClass('step-marked');
        $(this).addClass('step-marked');
        e.preventDefault();
      }
    } else {
      $(this).toggleClass('step-marked');
      e.preventDefault();
    }
  });

  $('.note-text').on('click', function(e) {
    $(this).parent().find('td').removeClass('item-marked');
    $(this).parent().find('td').toggleClass('item-complete');
    e.preventDefault();
  });



  console.log("Loaded Custom JS")
});
