/*
// This file is concatenated and compiled along with the other dependencies (it comes last).
// Other dependencies are jQuery and Bootstrap.
// See README.MD for more info on this (see the section about Grunt).
*/

/*
// AJAX Search functionality
// -------------------------
// Uses Typeahead.js and Bloodhound
// Typeahead is really nice for a single datasource..
// Toolbox has a single datasource.. 
// Typeahead is not nice for Toolbox.
// 
// The problem is, it seems to be impossible make headers for categories without supplying them all as datasources.
// The solution is an unsemantic code soup according to the developers. Their suggestion is to make a new hound model
// for each source, the a new Typeahead for each source too, static repeating code... I don't like code soup.
// So the below is more complex than it can be but there are less lines of code that do more.
// In the array just below you can define sources, the Bloodhounds and Typeaheads will be dynamically generated.
*/

// Create search categories array..
var arrSearchCategories = Array(
    {
        name    : 'adviezen',
        strclass: 'tb-adviezen',
        title   : 'Adviezen'
    },
    {
        name    : 'tools',
        strclass: 'tb-tools',
        title   : 'Tools'
    },
    {
        name    : 'categorie',
        strclass: 'tb-categorie',
        title   : 'Categorie'
    },
    {
        name    : 'platforms',
        strclass: 'tb-platforms',
        title   : 'Platformen'
    },
        {
        name    : 'playlist',
        strclass: 'tb-rocket',
        title   : 'Stappenplan'
    },
    {
        name    : 'messages',
        strclass: '',
        title   : 'Meldingen'
    }
);

var hounds      = new Object();
var typeaheads  = Array();

var CreateSearch = function()
{
    // loop through the categories
    $.each(arrSearchCategories, function(i,arr)
    {
        // make some hounds..
        hounds[arr.name] = new Bloodhound(
        {
            remote  : 
            {
                url: '/search/%QUERY/',
                filter: 
                    function (data) 
                    {
                        return data[arr.name];
                    }
            },
            datumTokenizer: function(d) 
            {
                return Bloodhound.tokenizers.whitespace(d.val);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace
        });
        
        // Init hounds..
        hounds[arr.name].initialize();
        
        // Make some typeaheads
        typeaheads.push( 
        {
            name        : arr.name,
            source      : hounds[arr.name].ttAdapter(),
            templates   :
            {
               header       :   function() // Template for headers in the searchresult dropdown..
                                {
                                    return '<p class="dropdown-header"><i class="'+arr.strclass+'"></i>'+arr.title+'</p>';
                                },
               suggestion   :   function(item) // Template for the searchresults.
                                {
                                    return '<a href="'+item.href+'"><p><i class="'+item.icon+'"></i>'+item.title+'</p></a>';
                                }
            }
        })
    });
    
    // Init the typeaheads..
    $("#search").typeahead(
        {
            minLength: 3,
            highlight: true,
            hint     : false
        },
        typeaheads
    )
    // Make sure the dropdown is visible in repsonisve mode..
    .on('typeahead:opened', function()
    {
        $(".navbar-collapse.in").css('overflow-y','visible');
    })
    .on('typeahead:closed', function()
    {
        $(".navbar-collapse.in").css('overflow-y','auto');
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
        var direction = "left";
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
    CreateSearch();
    // Initialise Bootstrap pop-overs 
    SetPopovers("body");
    
    var hidePopovers = function (e) 
    {
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
    
    $('body').on('touchend', hidePopovers);
    $('body').on('click', hidePopovers);
    
})


