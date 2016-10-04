/*手风琴列表 JS*/
$(function() {
  var Accordion = function(el, multiple) {
    this.el = el || {};
    this.multiple = multiple || false;

    // Variables privadas
    var links = this.el.find('.link');
    // Evento
    links.on('click', {
      el: this.el,
      multiple: this.multiple
    }, this.dropdown)
  }

  Accordion.prototype.dropdown = function(e) {
    var $el = e.data.el;
    $this = $(this),
      $next = $this.next();

    $next.slideToggle();
    $this.parent().toggleClass('open');

    if (!e.data.multiple) {
      $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
    };
  }

  var accordion = new Accordion($('#accordion'), false);
});

/*下拉效果*/

/*自动加入标签效果 更新内容*/

$().ready(function() {
  $(".Run").click(function() {
    $(".accordion").append('<li><div class="link"><i class="fa fa-paint-brush"></i>Diseno web<i class="fa fa-chevron-down"></i></div><ul class="submenu"><li><a href="#">Photoshop</a></li><li><a href="#">HTML</a></li><li><a href="#">CSS</a></li><li><a href="#">Maquetacion web</a></li></ul></li>');
  });
});

