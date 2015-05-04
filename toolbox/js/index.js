/*
// This file is concatenated and compiled along with the other dependencies (it comes last).
// Other dependencies are jQuery and Bootstrap.
// See README.MD for more info on this (see the section about Grunt).
*/

var suggest_box
var search_input
var spin_box
var resetSearch  = function(clear)
{
    if (clear === true)
    {
        search_input.val("");
    }
    suggest_box.empty();
    lastset = {}
    suggest_box.parent().removeClass('open');
    spinner(false);
}
var spinner = function(spinning)
{
    if (spinning===true)
    {
        $(spin_box).removeClass("stopped").addClass("spinning");
    }
    else if(spinning===false)
    {
        $(spin_box).removeClass("spinning").addClass("stopped");
    }
}
var CreateSearch = function(input)
{
    settings        = {'minLength':3};
    cache           = [];
    lastset         = {};
    suggest_box     = input.siblings("ul.search-results");
    search_input    = input
    spin_box        = input.siblings(".spinner");
    var timeout;
    
    // loop through the categories
    var fetch = function(query,callback)
    {
        if (query in cache)
        {   
            callback(cache[query]);
        } 
        else 
        {
            $.get("/search/"+encodeURIComponent(query)+"/")
            .done(function(data) 
            {   
                cache[query] = data;
                callback(data,query);
            })
            .fail(function() 
            {
                callback({'errors':
                            {
                                'icon':'tb-warning',
                                'title':'Er ging helaas iets mis..',
                                'suggestions':
                                [{
                                    'href':'/doc/contact/',
                                    'title':'Klik hier om een probleem te melden.',
                                    'icon':'tb-warning'
                                }]
                            }},query);
            })
            .always(function() 
            {
                spinner(false);
            });
        }
    };
    
    var parseData = function(data, query)
    {
        if (data === lastset)
        {
            return false;            
        }
        lastset = data
        suggest_box.empty();
        results = 0;
        $.each(data,function()
        {
            if (this.suggestions.length > 0)
            {
                $(suggest_box).append(
                    $("<li>")
                        .addClass("dropdown-header")
                        .addClass(this.icon)
                        .attr('role',"presentation")
                        .html(this.title)
                );
                $.each(this.suggestions,function()
                {
                    var re = RegExp("("+query+")",'gi');
                    $(suggest_box).append(
                        $("<li>").append(
                            $("<a>")
                                .html(this.title.replace(re,"<strong>$1</strong>"))
                                .addClass(this.icon)
                                .attr('href',this.href)
                                .attr('tabindex','0')
                                .addClass('suggestion')
                        )
                    );
                    results++;
                });
            }
        });
        if (results === 0)
        {
            resetSearch();
        }
        else
        {
            input.dropdown('toggle');
        }
    }
    
    input.keyup(function(key)
    {   
        if (key.keyCode == 27)
        {
            resetSearch(true);
        }
        else
        {
            query = $(this).val();
            if(query.length >= settings.minLength)
            {
                spinner(true);
                clearTimeout(timeout);
                timeout = setTimeout(function() {
                     fetch(query,parseData);
                }, 300);
                
            }
            else
            {
                resetSearch();
            }
        }
    });
    
    suggest_box.keyup(function(key)
    {
       if (key.keyCode == 27)
       {
           resetSearch();
       } 
    });
}


var SetPopovers = function(elements)
{
    var selector = elements+' abbr:not([id^=abbr-])';
    if (elements==="body")
    {
        selector +=', span[data-toggle="popover"]';
    }
    $(selector).each(function()
    {   
        var direction = "bottom";
        if ($(this).prop('nodeName')==="ABBR")
        {
            direction = "bottom";
            $(this)
                .attr("data-content", $(this).attr("title"))
                .attr("title","Definitie: "+$(this).text()) 
                .attr("data-toggle","popover");
        }
        $(this).popover(
        {
            "animation" : true,
            "container" : "body",
            "html"      : true,
            "trigger"   : "click",
            "placement" : direction,
        }).on("shown.bs.popover",function()
        {
            SetPopovers("#"+$(this).attr('aria-describedby'));
        }).on("hide.bs.popover", function()
        {
            KillTheChildren($(this).attr('aria-describedby'));
        }).on("show.bs.popover",function()
        {
            if (elements==="body")
            {
                KillAllExcept($(this).attr('aria-describedby'));
            } else {
                KillTheChildren($(this).parents(".popover").attr('id'));
            };
        });
    });
}

// Well this is awkward..
var KillTheChildren = function(id)
{
    $('#'+id+' [data-toggle="popover"]').each(function()
    {
        $('#'+KillTheChildren($(this).attr('aria-describedby'))).popover('hide');
    });
    return id;
}
var KillAllExcept = function(id)
{
    $('[data-toggle="popover"]').each(function () 
    {
        if ($(this).attr("aria-describedby")!==id)
        {
            $(this).popover('hide');
        }
    });
}

$(document).ready(function()
{    
    // Init the typeaheads..
    CreateSearch($("#search"));
    // Initialise Bootstrap pop-overs 
    SetPopovers("body");
    
    var resetElements = function (e) 
    {
        // Hide search dropdown
        if (e.target.id !=="search" && !$("#search").siblings(".search-results").has(e.target).length)
        {
            resetSearch(true)
        }
        // Hide popovers..
        if (e.target.nodeName!="ABBR" && !(e.target.nodeName==="SPAN" && $(e.target).attr('data-toggle')==="popover"))
        {
            var none_of_these=true;
            $('.popover').each(function () 
            {
                if($(this).is(e.target) || $(this).has(e.target).length)
                {
                    KillTheChildren($(this).attr("id"));
                    none_of_these=false;
                }
            });
            if (none_of_these===true)
            {
                KillAllExcept(-1);
            }
        }
    }
    
    $('body').on('touchend', resetElements);
    $('body').on('click', resetElements);
    var player_height = $(window).height()/1.5
    if (player_height > 720) {player_height=720}
    $("#intro-video").height(player_height);
})


