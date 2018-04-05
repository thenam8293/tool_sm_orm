// Auto display div label after input
$(document).ready(function(){
    if ($('select').val() != '') {
        $('.select').fadeIn(500);
    }
    $(".select").parents().css("position", "relative");
    $(".select").parents().css("margin-bottom", "1.5em");
    $('select').on('change', function (){
        $(this).parent().children('.select').fadeIn(500);
    });
});

// End Auto display div label after input

// Auto display label after input
/* Float Label Pattern Plugin for Bootstrap 3.1.0 by Travis Wilson */
$(function($){
    $.fn.floatLabels = function (options) {
        // Settings
        var self = this;
        var settings = $.extend({}, options);
        // Event Handlers
        function registerEventHandlers() {
            self.on('input keyup change', 'input,select, textarea', function () {
                actions.swapLabels(this);
            });
        }
        // Actions
        var actions = {
            initialize: function() {
                self.each(function () {
                    var $this = $(this);
                    var $label = $this.children('label');
                    var $field = $this.find('input,select,textarea').first();
                    if ($this.children().first().is('label')) {
                        $this.children().first().remove();
                        $this.append($label);
                    }
                    var placeholderText = ($field.attr('placeholder') && $field.attr('placeholder') != $label.text()) ? $field.attr('placeholder') : $label.text();
                    $label.data('placeholder-text', placeholderText);
                    $label.data('original-text', $label.text());
                    if ($field.val() == '') {
                        $field.addClass('empty')
                    }
                });
            },
            swapLabels: function (field) {
                var $field = $(field);
                var $label = $(field).siblings('label').first();
                var isEmpty = Boolean($field.val());
                if (isEmpty) {
                    $field.removeClass('empty');
                    $label.text($label.data('original-text'));
                }
                else {
                    $field.addClass('empty');
                    $label.text($label.data('placeholder-text'));
                }
            }
        }
        // Initialization
        function init() {
            registerEventHandlers();

            actions.initialize();
            self.each(function () {
                actions.swapLabels($(this).find('input,select,textarea').first());
            });
        }
        init();
        return this;
    };
    $(function () {
        $('.float-label-control').floatLabels();
    });
});
// End Auto display label after input


// Auto add dots when input number
function reverseNumber(input) {
    return [].map.call(input, function(x) {
        return x;
    }).reverse().join(''); 
}
  
function plainNumber(number) {
    return number.split('.').join('');
}
  
function splitInDots(input) {
    var value = input.value,
        plain = plainNumber(value),
        reversed = reverseNumber(plain),
        reversedWithDots = reversed.match(/.{1,3}/g).join('.'),
        normal = reverseNumber(reversedWithDots);
    console.log(plain,reversed, reversedWithDots, normal);
    input.value = normal;
}
function oneDot(input) {
    var value = input.value,
        value = plainNumber(value);
    if (value.length > 3) {
        value = value.substring(0, value.length - 3) + '.' + value.substring(value.length - 3, value.length);
    }
    console.log(value);
    input.value = value;
}
// End Auto add dots when input number

// Enable Confirmation
$(document).ready(function(){
    $('#send_meeting,#save,#start').confirmation({
        rootSelector: '[data-toggle=confirmation-singleton]',
        container: 'body'
    });
});
$(document).ready(function() {
    $('#noi_dung').multiselect({
        buttonWidth: '100%',
        includeSelectAllOption: true,
        onChange: function(element, checked) {
        }
    });
    $('#thanh_vien').multiselect({
        buttonWidth: '100%',
        includeSelectAllOption: true,
        onChange: function(element, checked) {
        }
    });
    $('#luu_ho_so').multiselect({
        buttonWidth: '100%',
        includeSelectAllOption: true,
        onChange: function(element, checked) {
        }
    });
});
// End Enable Confirmation

// Functions
function checkCurrentTabs() {
    $('.finish').prop('disabled',true);
    if ($('#thong_tin_chung').attr('class').indexOf("active") < 0) {
        $('#dots-Draft').css('display','none');
        $('#dots').css('display','');
    } else {
        $('#dots-Draft').css('display','');
        $('#dots').css('display','none');
    }
};
function enableStart_CheckMandatory() {
    $("#start").prop("disabled",false).removeClass('btn-default').addClass('btn-danger');
};
function redirectOfficial() {
    location.href='official';
}; 
function CheckHS() {
    if ($('#to_trinh_checkbox').is(':checked') && $('#YKT_checkbox').is(':checked')) {
        $("#send_meeting").prop('disabled',false).removeClass('btn-default').addClass('btn-warning');
    } else {
        $("#send_meeting").prop('disabled',true).addClass('btn-default').removeClass('btn-warning');
        $("#start").prop('disabled',true).removeClass('btn-danger').addClass('btn-default');
    }
}
// End Functions