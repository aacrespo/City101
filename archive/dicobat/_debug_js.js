ï»¿// Premium ou public
var isPublic = $(document.body).is('.public-user');

// Nano scroller
$(".nano").nanoScroller();

// Lightbox
$('a.lightbox').fancybox();
$('a.colorbox').fancybox();

// Placeholder recherche
(function () {
    // Check
    if ('placeholder' in document.createElement('input')) return;
    var input = $('#recherche input[type="text"]');
    var value = input.attr('placeholder');
    var place = $('<span class="placeholder"/>');
    place.text(value).insertBefore(input);
    place.on('click focus', function () {
        input.trigger('focus');
    });
    input.on('keyup focus blur', function () {
        place.text(this.value.length ? '' : value);
    });
}());

// Menu sidebar
(function () {
    // Variables
    var posY = 10;
    var wrap = $('#nav_onglets');
    var curr = wrap.data('active') || 0;
    var btns = wrap.find('.un_element a');
    var tabs = wrap.find('.contenu_onglet');
    // Process
    btns.each(function (i) {
        $(this).data('index', i);
    }).on('click', function (e) {
        // Variables
        var btn = $(this);
        var idx = btn.data('index');
        var tab = tabs.eq(idx);
        // Display
        btns.not(btn).removeClass('active');
        btn.addClass('active');
        tabs.not(tab).hide();
        tab.show();
        // No propag
        e.preventDefault();
        e.stopPropagation();
    }).eq(curr).click();
    // Autofixed
    posY = wrap.offset().top - posY;
    $(window).on('scroll', function () {
        var isFixed = $(window).scrollTop() > posY;
        wrap.toggleClass('isFixed', isFixed);
    });
}());


// Scroll to top
(function () {
    // Variables
    var height = 200;
    var button = $('<a id="top_page"/>');
    // Init
    button.appendTo(document.body);
    // Events
    $(window).on('scroll', function () {
        var visible = $(window).scrollTop() > height;
        button.toggleClass('visible', visible);
    });
    button.on('click', function () {
        $('html, body').animate({scrollTop: 0}, 600);
    });
}());


// Flips Page dÃ©tails produit
$('.flipproduit').on('click', function () {
    var button = $(this);
    var href = button.data('href');

    $.fancybox.open(href, {
        type: 'iframe',
        iframe: {preload: false, scrolling: 'no'},
        width: 1900, height: 1500, aspectRatio: true
    });
    return false;
});


// Slide accueil
$('#le-slide').each(function () {
    // Variables
    var wrap = $(this);
    var buttons = wrap.children().eq(0);
    var elements = wrap.children().eq(1);
    var a = {i: {s: 400, d: 0}, h: {s: 400, d: 200}, b: {s: 400, d: 400}};
    a.t = 600; //Math.max(a.i.s+a.i.d, a.h.s+a.h.d, a.b.s+a.b.d);
    // Create buttons
    buttons.empty();
    elements.children().each(function () {
        // Variables
        var title = $(this).find('.titre span').first().clone().addClass('titre');
        var descr = $(this).find('.titre p').first().clone();
        var image = $(this).find('img').first().clone();
        var wrap = $('<div/>').addClass('un_element');
        var link = $('<a/>');
        // Storage
        $(this).data('dcbt-items', {
            i: $(this).find('img').first(),
            h: $(this).find('.haut').first(),
            b: $(this).find('.bas').first()
        });
        // Modif DOM
        link.append([image, title, descr]);
        wrap.append(link).appendTo(buttons);
    });
    // Events
    elements.on('dcbt-show', '.un_element', function () {
        // Variables
        var block = $(this);
        var items = block.data('dcbt-items');
        // Process
        block.addClass('current');
        items.i.stop(true).delay(a.t + a.i.d).animate({top: 20, opacity: 1}, a.i.s);
        items.h.stop(true).delay(a.t + a.h.d).animate({left: 224, opacity: 1}, a.h.s);
        items.b.stop(true).delay(a.t + a.b.d).animate({bottom: 20, opacity: 1}, a.b.s);
    }).on('dcbt-hide', '.un_element', function () {
        // Variables
        var block = $(this);
        var items = block.data('dcbt-items');
        // Process
        block.removeClass('current');
        items.i.stop(true).delay(a.i.d).animate({top: -400, opacity: 0}, a.i.s);
        items.h.stop(true).delay(a.h.d).animate({left: 900, opacity: 0}, a.h.s);
        items.b.stop(true).delay(a.b.d).animate({bottom: -150, opacity: 0}, a.b.s);
    });
    buttons.on('click', '.un_element', function () {
        // Variables
        var index = $(this).prevAll().length;
        var curr = elements.children('.current');
        var next = elements.children().eq(index);
        // Process
        $(this).addClass('current').siblings().removeClass('current');
        setTimeout(function () {
            curr.trigger('dcbt-hide');
        }, 1);
        setTimeout(function () {
            next.trigger('dcbt-show');
        }, curr.length ? a.t : 1);
    });
    // Quick display
    (function () {
        var o = a;
        a = {i: {s: 0, d: 0}, h: {s: 0, d: 0}, b: {s: 0, d: 0}};
        elements.children().trigger('dcbt-hide');
        buttons.children().first().trigger('click');
        a = o;
    })();
    // Auto run
    (function () {
        // Check mouse over
        var hover = false;
        wrap.on('mouseenter', function () {
            hover = true;
        });
        wrap.on('mouseleave', function () {
            hover = false;
        });
        // Next slide
        setInterval(function () {
            if (hover) return;
            var btn = buttons.children('.current').next();
            if (!btn.length) btn = buttons.children().first();
            btn.trigger('click');
        }, 5000);
    })();
    // Flips
    wrap.on('click', '.flip', function () {
        var button = $(this);
        var href = button.data('href');

        $.fancybox.open(href, {
            type: 'iframe',
            iframe: {preload: false, scrolling: 'no'},
            width: 1900, height: 1500, aspectRatio: true
        });
        return false;
    });
});
// Slide accueil
$('#le-slide2').each(function () {
    // Variables
    var wrap = $(this);
    var buttons = wrap.children().eq(0);
    var elements = wrap.children().eq(1);
    var a = {i: {s: 400, d: 0}, h: {s: 400, d: 200}, b: {s: 400, d: 400}};
    a.t = 600; //Math.max(a.i.s+a.i.d, a.h.s+a.h.d, a.b.s+a.b.d);
    // Create buttons
    buttons.empty();
    elements.children().each(function () {
        // Variables
        var title = $(this).find('.titre span').first().clone().addClass('titre');
        var descr = $(this).find('.titre p strong').first().clone();
        var descr2 = $(this).find('.titre p .text-hide').first().clone();
        var image = $(this).find('img').first().clone();
        var wrap = $('<div/>').addClass('un_element');
        var link = $('<a/>');
        // Storage
        $(this).data('dcbt-items', {
            i: $(this).find('img').first(),
            h: $(this).find('.haut').first(),
            b: $(this).find('.bas').first()
        });
        // Modif DOM
        link.append([image, title,'<br/>', descr2, descr]);
        wrap.append(link).appendTo(buttons);
    });
    // Events
    elements.on('dcbt-show', '.un_element', function () {
        // Variables
        var block = $(this);
        var items = block.data('dcbt-items');
        // Process
        block.addClass('current');
        items.i.stop(true).delay(a.t + a.i.d).animate({top: 20, opacity: 1}, a.i.s);
        items.h.stop(true).delay(a.t + a.h.d).animate({left: 224, opacity: 1}, a.h.s);
        items.b.stop(true).delay(a.t + a.b.d).animate({bottom: 20, opacity: 1}, a.b.s);
    }).on('dcbt-hide', '.un_element', function () {
        // Variables
        var block = $(this);
        var items = block.data('dcbt-items');
        // Process
        block.removeClass('current');
        items.i.stop(true).delay(a.i.d).animate({top: -400, opacity: 0}, a.i.s);
        items.h.stop(true).delay(a.h.d).animate({left: 900, opacity: 0}, a.h.s);
        items.b.stop(true).delay(a.b.d).animate({bottom: -150, opacity: 0}, a.b.s);
    });
    buttons.on('click', '.un_element', function () {
        // Variables
        var index = $(this).prevAll().length;
        var curr = elements.children('.current');
        var next = elements.children().eq(index);
        // Process
        $(this).addClass('current').siblings().removeClass('current');
        setTimeout(function () {
            curr.trigger('dcbt-hide');
        }, 1);
        setTimeout(function () {
            next.trigger('dcbt-show');
        }, curr.length ? a.t : 1);
    });
    // Quick display
    (function () {
        var o = a;
        a = {i: {s: 0, d: 0}, h: {s: 0, d: 0}, b: {s: 0, d: 0}};
        elements.children().trigger('dcbt-hide');
        buttons.children().first().trigger('click');
        a = o;
    })();
    // Auto run
    (function () {
        // Check mouse over
        var hover = false;
        wrap.on('mouseenter', function () {
            hover = true;
        });
        wrap.on('mouseleave', function () {
            hover = false;
        });
        // Next slide
        setInterval(function () {
            if (hover) return;
            var btn = buttons.children('.current').next();
            if (!btn.length) btn = buttons.children().first();
            btn.trigger('click');
        }, 5000);
    })();
    // Flips
    wrap.on('click', '.flip', function () {
        var button = $(this);
        var href = button.data('href');

        $.fancybox.open(href, {
            type: 'iframe',
            iframe: {preload: false, scrolling: 'no'},
            width: 1900, height: 1500, aspectRatio: true
        });
        return false;
    });
});

if ($('.visuel-bat-element-custom').length) {
    $('#slideList')
        .find('.un_element:last-child p')
        .replaceWith('<p>Tout le Dicobat en ligne<br /> <strong style="color: rgb(141, 17, 21);">Abonnement Premium</strong></p>');
}


// Slide illustrations
$('#illustrations_content').clide({
    index: 0,
    speed: 1000,
    delay: 4000,
    effect: 'hslide',
    controls: {
        prev: '#prev_slide',
        next: '#next_slide'
    },
    auto: {enable: true, pause: true},
    anim: [
        {zIndex: 10},
        {zIndex: 20}
    ]
});

// Limitations pour les visiteurs
// -> Pour info, c'est juste visuel
// -> Et y'a un check serveur Ã©videmment
if (isPublic) (function () {
    // RÃ©cupÃ©ration de l'image "premium"
    var premiumImage = $('#sidebar a.premium').clone().wrap('<div/>').parent();
    var premiumPopup = function () {
        $.fancybox.open(premiumImage);
        return false;
    };
    // Recherche anglaise
    (function () {
        // Variables
        var label = $('#recherche label.en');
        var input = label.find('input').first();
        // Update display
        $('<i/>').css({
            cursor: 'not-allowed',
            position: 'absolute',
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        }).appendTo(label);
        label.css({position: 'relative', color: '#888'}).attr('title', 'FonctionnalitÃ© rÃ©servÃ©e aux membres premium');
        input.prop('disabled', true).removeAttr('name');
        // Event
        label.on('click', premiumPopup);
    }());
}());

// Generateur de regex
var RegexBuilder = (function () {
    // Variables
    var i, char, chars, group, regex;
    var cache = {};
    // Liste des regles
    var rules = [
        ['a', 'Ã Ã¡Ã¢Ã£Ã¤Ã¥'],
        ['e', 'Ã¨Ã©ÃªÃ«'],
        ['i', 'Ã¬Ã­Ã®Ã¯'],
        ['o', 'Ã²Ã³Ã´ÃµÃ¶Ã¸'],
        ['u', 'Ã¹ÃºÃ»Ã¼'],
        ['y', 'Ã½Ã¿'],
        ['c', 'Ã§'],
        ['n', 'Ã±']
    ];
    // PrÃ©traitement
    for (i = rules.length - 1; i >= 0; i--) {
        char = rules[i][0];
        chars = rules[i][1];
        group = '[' + char + chars + ']';
        regex = new RegExp(group, 'ig');
        rules[i] = {char: char, chars: chars, group: group, regex: regex};
    }
    // CrÃ©ation de la fonction
    var Builder = function (src) {
        // VÃ©rification du cache
        if (cache.hasOwnProperty(src)) return cache[src];
        // PrÃ©paration de la regex
        var dst = src;
        for (i = rules.length - 1; i >= 0; i--) dst = dst.replace(rules[i].regex, rules[i].char);
        dst = dst.replace(/[^a-z0-9 ]/ig, '.').replace(/[.][.]+/ig, '.+?');
        for (i = rules.length - 1; i >= 0; i--) dst = dst.replace(rules[i].regex, rules[i].group);
        // CrÃ©ation, mise en cache, et retour
        dst = new RegExp('(' + dst + ')', 'ig');
        cache[src] = dst;
        return dst;
    };
    return Builder;
}());

// AutocomplÃ©tion
(function () {
    // Variables
    var form = $('#recherche form').first();
    var term = form.find('input[name="term"]');
    var lang = form.find('input[name="lang"]');
    var params = {ajax: true, lang: lang.val()};
    // Autocomplete
    term.autocomplete({
        minChars: 1,
        params: params,
        dataType: 'json',
        paramName: 'term',
        serviceUrl: '/recherche',
        triggerSelectOnValidInput: false,
        formatResult: function (suggestion, input) {
            var value = suggestion.value;
            var regex = RegexBuilder(input);
            var value = suggestion.value.replace(regex, '<b>$1<\/b>');
            if (suggestion.data.domain) value = value + '<i>(' + suggestion.data.domain + ')</i>';
            // if (suggestion.data.premium) value = '<span class="premium-icon"></span>' + value;
            if (suggestion.data.priority) value = '[' + suggestion.data.priority + '] ' + value;
            return value;
        },
        onSelect: function (suggestion) {
            document.location = suggestion.data.link;
        }
    });
    // Events
    lang.on('change', function () {
        params = {ajax: true, lang: lang.filter(':checked').val()};
        term.autocomplete().setOptions({params: params});
        term.autocomplete().clear();
    });
}());


// Init scrolls events
$(window).trigger('scroll');

$(document).ready(function(){
    $('.btn-menu').click(function(){
        $('.btn-menu').toggleClass('fa-times');
        $('.btn-menu').toggleClass('fa-bars');
        $('.menu-items').toggleClass('active');
        $('.logo-menu-responsive').toggleClass('active');
        $('.form-menu-responsive').toggleClass('active');
        $('body').toggleClass('overflow-hidden');
    })
})

$(document).ready(function(){
    $('.themes').click(function(){
        $('#sidebar').toggleClass('z-index-1001');
        $('#contenu_onglets').toggleClass('height-content-sidebar');
        $('#contenu_onglets').toggleClass('height-0');
        $('#sidebar div#onglets .un_element').toggleClass('width-auto');
    })
})


var smallBreak = 800; // Your small screen breakpoint in pixels
var columns = $('.dataTable tr').length;
var rows = $('.dataTable th').length;

$(document).ready(shapeTable());
$(window).resize(function() {
    shapeTable();
});

function shapeTable() {
    if ($(window).width() < smallBreak) {
        for (i=0;i < rows; i++) {
            var maxHeight = $('.dataTable th:nth-child(' + i + ')').outerHeight();
            for (j=0; j < columns; j++) {
                if ($('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').outerHeight() > maxHeight) {
                    maxHeight = $('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').outerHeight();
                }
                if ($('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').prop('scrollHeight') > $('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').outerHeight()) {
                    maxHeight = $('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').prop('scrollHeight');
                }
            }
            for (j=0; j < columns; j++) {
                $('.dataTable tr:nth-child(' + j + ') td:nth-child(' + i + ')').css('height',maxHeight);
                $('.dataTable th:nth-child(' + i + ')').css('height',maxHeight);
            }
        }
    } else {
        $('.dataTable td, .dataTable th').removeAttr('style');
    }
}

$(document).ready(function () {
    $('.logout-footer-button').click(function () {
        $.ajax({
            method: 'POST',
            url: '/ctrl_login.php',
            data: {
                op: 'deconnect'
            },
            success: function(response) {
                window.location.href = '/';
            }
        })
    })
})