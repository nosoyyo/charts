(function($) {
    "use strict";

    $.fn.fireOnDisable = function(settings) {
        // Only perform this DOM change if we have to watch changes with propertychange
        // Also only perform if getOwnPropertyDescriptor exists - IE>=8
        // I suppose I could test for "propertychange fires, but not when form element is disabled" - but it would be overkill
        if (!('onpropertychange'in document.createElement('input')) || Object.getOwnPropertyDescriptor === undefined) {
            return this;
        }

        // IE9-10 use HTMLElement proto, IE8 uses Element proto
        var someProto = window.HTMLElement === undefined ? window.Element.prototype : window.HTMLElement.prototype
          , someTrigger = function() {}
          , origDisabled = Object.getOwnPropertyDescriptor(someProto, 'disabled');

        if (document.createEvent) {
            someTrigger = function(newVal) {
                var event = document.createEvent('MutationEvent');
                /*
        Instantiate the event as close to native as possible:
        event.initMutationEvent(eventType, canBubble, cancelable, relatedNodeArg, prevValueArg, newValueArg, attrNameArg, attrChangeArg);
        */
                event.initMutationEvent('DOMAttrModified', true, false, this.getAttributeNode('disabled'), '', '', 'disabled', 1);
                this.dispatchEvent(event);
            }
            ;
        } else if (document.fireEvent) {
            someTrigger = function() {
                this.fireEvent('onpropertychange');
            }
            ;
        }

        return this.each(function() {
            // call prototype's set, and then trigger the change.
            Object.defineProperty(this, 'disabled', {
                set: function(isDisabled) {
                    // We store preDisabled here, so that when we inquire as to the result after throwing the event, it will be accurate
                    // We can't throw the event after the native send, because it won't be be sent.
                    // We must do a native fire/dispatch, because native listeners don't catch jquery trigger 'propertychange' events
                    $.data(this, 'preDisabled', isDisabled);
                    if (isDisabled) {
                        // Trigger with dispatchEvent
                        someTrigger.call(this, isDisabled);
                    }

                    return origDisabled.set.call(this, isDisabled);
                },
                get: function() {
                    var isDisabled = $.data(this, 'preDisabled');
                    if (isDisabled === undefined) {
                        isDisabled = origDisabled.get.call(this);
                    }
                    return isDisabled;
                }
            });
        });
    }
    ;
}
)(jQuery);

$(function() {
    if ($.fn.lazyload) {
        $(".lazy").lazyload();
    }

    $.fn.datepicker.defaults.language = "zh-CN";
    $.fn.datepicker.defaults.format = "yyyy-mm-dd";
    $.fn.datepicker.defaults.autoclose = true;

    $('.bs-date-picker').length && $('.bs-date-picker').datepicker({
        format: "yyyy-mm-dd"
    });

    if ($.fn.select2) {
        $.fn.select2.defaults.set("minimumResultsForSearch", "Infinity");
        $.fn.select2.defaults.set("language", "zh-CN");
        $('.select2-select').length && $('.select2-select').fireOnDisable().select2({});
    }

    setTimeout(function() {
        $('.toplist_nav').affix({
            offset: {
                top: 60,
                bottom: 100
            }
        })

        $(window).trigger('scroll')
        if ($(window).scrollTop() > 0) {
            $(window).scrollTop($(window).scrollTop() - 1)
        }
    }, 100)
})
