                                            
var command = [ 
                { 
                    'type'   : "output",
                    'string' : "[18/Jul/2014 16:49:42] \x22GET /error/404/ HTTP/1.1\x22 404 1807"
                },
                { 
                    'type'   : "command",
                    'string' : "echo \x27Volgens mij gaat er iets mis....\x27",
                },
                { 
                    'type'   : "output",
                    'string' : "Volgens mij gaat er iets mis...."
                },
                { 
                    'type'   : "command",
                    'string' : "echo \x27Even kijken wat er aan de hand is..\x27",
                },
                { 
                    'type'   : "output",
                    'string' : "Even kijken wat er aan de hand is.."
                },
                {
                    'type'   : 'command',
                    'string' : 'clear'
                },
                { 
                    'type'   : "command",
                    'string' : "nginx --show-error -vvv"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0xeee\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0.n~~%x.\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0xeee\xA0\xA0\xA0\xA0"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0\xA0\xA0d888R\xA0\xA0\xA0\xA0\xA0\xA0\xA0x88X\xA0\xA0\xA0888.\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0d888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0\xA0d8888R\xA0\xA0\xA0\xA0\xA0X888X\xA0\xA0\xA08888L\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0d8888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0@\xA08888R\xA0\xA0\xA0\xA0X8888X\xA0\xA0\xA088888\xA0\xA0\xA0\xA0\xA0\xA0\xA0@\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0.P\xA0\xA08888R\xA0\xA0\xA0\xA088888X\xA0\xA0\xA088888X\xA0\xA0\xA0\xA0.P\xA0\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0:F\xA0\xA0\xA08888R\xA0\xA0\xA0\xA088888X\xA0\xA0\xA088888X\xA0\xA0\xA0:F\xA0\xA0\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0x\x22\xA0\xA0\xA0\xA08888R\xA0\xA0\xA0\xA088888X\xA0\xA0\xA088888f\xA0\xA0x\x22\xA0\xA0\xA0\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "d8eeeee88888eer\xA048888X\xA0\xA0\xA088888\xA0\xA0d8eeeee88888eer"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0\xA0\xA08888R\xA0\xA0\xA0\xA0\xA0?888X\xA0\xA0\xA08888\x22\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\xA0\xA0\xA08888R\xA0\xA0\xA0\xA0\xA0\xA0\x2288X\xA0\xA0\xA088*`\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA08888R"
                },
                { 
                    'type'   : "output",
                    'string' : "\xA0\xA0\xA0\xA0\x22*%%%%%%**~\xA0\xA0\xA0\xA0\xA0^\x22===\x22`\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\xA0\x22*%%%%%%**~"
                }
                ,
                { 
                    'type'   : "command",
                    'string' : ""
                }

              ]
    
    var licmd    = '<li class="command"></li>';
    var liplain  = '<li></li>';
    var delays   = 
    {
        'output'  : {'min':3,'max':6},
        'command'  : {'min':80,'max':140},
        //'output'  : {'min':3,'max':4},
        //'command'  : {'min':10,'max':20},
    }
    
    var ShellPrint = function()
    {
        var shell = $("#shell");
        // Start the printing process...
        setTimeout( function()
        {
            PrintSTDOUT(shell, 0, false, 0);
        }, 500 );
    }
    
    var ClearSTDOUT = function()
    {
        $("#shell").empty();
    }
    
    var PrintSTDOUT = function(shell, intCmd, li, intChar)
    {
        cmd = command[intCmd]['string']
        type =  command[intCmd]['type']

        // We need to create a new line..
        if (li === false)
        {
            // New line with shell prompt
            if (type == "command")
            {
                li = $(licmd).appendTo(shell);
            }
            // New line without shell prompt
            else
            {
                li = $(liplain).appendTo(shell);
            }
        }
        
        if (intChar < cmd.length)
        {
            // Print a character
            $(li).append(cmd[intChar]);
            
            var timeout = Math.random() * (delays[type]['max'] - delays[type]['min']) + delays[type]['min']; 
            
            // Set timeout for next character
            setTimeout( function()
            {
                PrintSTDOUT(shell, intCmd, li, intChar+1);
            }, timeout );
        }
        // End of line reached..
        else
        {
            if (cmd == "clear")
            {
                setTimeout(ClearSTDOUT, 500 );
            }
            // Select next line and end the current line..
            if (intCmd+1 < command.length)
            {
                setTimeout( function()
                {
                    PrintSTDOUT(shell, intCmd+1, false, 0);
                }, 500 );
            }
        }
    }
    
    
$(document).ready(function()
{    
    ShellPrint();
});