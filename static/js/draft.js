

// Animation chuyền Tab
    $('a[data-toggle="tab"]').on('hide.bs.tab', function (e) {
        var $old_tab = $($(e.target).attr("href"));
        var $new_tab = $($(e.relatedTarget).attr("href"));

        if($new_tab.index() < $old_tab.index()){
            $old_tab.css('position', 'relative').css("right", "0").show();
            $old_tab.animate({"right":"-100%"}, 300, function () {
                $old_tab.css("right", 0).removeAttr("style");
            });
        }
        else {
            $old_tab.css('position', 'relative').css("left", "0").show();
            $old_tab.animate({"left":"-100%"}, 300, function () {
                $old_tab.css("left", 0).removeAttr("style");
            });
        }
    });
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        var $new_tab = $($(e.target).attr("href"));
        var $old_tab = $($(e.relatedTarget).attr("href"));

        if($new_tab.index() > $old_tab.index()){
            $new_tab.css('position', 'relative').css("right", "-2500px");
            $new_tab.animate({"right":"0"}, 500);
        }
        else {
            $new_tab.css('position', 'relative').css("left", "-2500px");
            $new_tab.animate({"left":"0"}, 500);
        }
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        // your code on active tab shown
    });
//End Animation chuyền

//Chuyền Tabs onClick
    $('.btnNext').click(function(){
        $('.nav-tabs > .active').next('li').find('a').trigger('click');
    });
    $('.btnPrevious').click(function(){
        $('.nav-tabs > .active').prev('li').find('a').trigger('click');
    });
//End Chuyền Tabs onClick

    jQuery(document).ready(function($){
        // browser window scroll (in pixels) after which the "back to top" link is shown
        var offset = 300,
            //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
            offset_opacity = 1200,
            //duration of the top scrolling animation (in ms)
            scroll_top_duration = 700,
            //grab the "back to top" link
            $back_to_top = $('.cd-top');

        //hide or show the "back to top" link
        $(window).scroll(function(){
            ($(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
            if( $(this).scrollTop() > offset_opacity ) { 
                $back_to_top.addClass('cd-fade-out');
            }
        });
        //smooth scroll to top
        $back_to_top.on('click', function(event){
            event.preventDefault();
            $('body,html').animate({
                scrollTop: 0 ,
                }, scroll_top_duration
            );
        });
    });

// Chuyển Tabs
    $("ul.nav-tabs a").click(function (e) {
      e.preventDefault();  
        $(this).tab('show');
    });
// End Chuyển Tabs

//panel_body
    $(document).ready(function() {
        $(".toggle-accordion").on("click", function() {
            var accordionId = $(this).attr("accordion-id"),
            numPanelOpen = $(accordionId + ' .collapse.in').length;
        $(this).toggleClass("active");
        if (numPanelOpen == 0) {
            openAllPanels(accordionId);
        } else {
            closeAllPanels(accordionId);
        }
    })
        openAllPanels = function(aId) {
            console.log("setAllPanelOpen");
            $(aId + ' .panel-collapse:not(".in")').collapse('show');
        }
        closeAllPanels = function(aId) {
            console.log("setAllPanelclose");
            $(aId + ' .panel-collapse.in').collapse('hide');
        }     
    });
//End panel_body