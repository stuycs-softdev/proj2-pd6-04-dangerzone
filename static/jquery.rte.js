/*
 * jQuery RTE plugin 0.3 - create a rich text form for Mozilla, Opera, and Internet Explorer
 *
 * Copyright (c) 2007 Batiste Bieler
 * Distributed under the GPL (GPL-LICENSE.txt) licenses.
 *
 * Modifications by Ben Kurtovic, 2013.
 */

// define the rte light plugin
jQuery.fn.rte = function(css_url, media_url) {

    if(document.designMode || document.contentEditable)
    {
        $(this).each( function(){
            var textarea = $(this);
            enableDesignMode(textarea);
        });
    }

    function formatText(iframe, command, option) {
        iframe.contentWindow.focus();
        try{
            iframe.contentWindow.document.execCommand(command, false, option);
        }catch(e){console.log(e)}
        iframe.contentWindow.focus();
    }

    function tryEnableDesignMode(iframe, doc, callback) {
        try {
            iframe.contentWindow.document.open();
            iframe.contentWindow.document.write(doc);
            iframe.contentWindow.document.close();
        } catch(error) {
            console.log(error)
        }
        if (document.contentEditable) {
            iframe.contentWindow.document.designMode = "On";
            callback();
            return true;
        }
        else if (document.designMode != null) {
            try {
                iframe.contentWindow.document.designMode = "on";
                callback();
                return true;
            } catch (error) {
                console.log(error)
            }
        }
        setTimeout(function(){tryEnableDesignMode(iframe, doc, callback)}, 250);
        return false;
    }

    function enableDesignMode(textarea) {
        // need to be created this way
        var iframe = document.createElement("iframe");
        iframe.frameBorder=0;
        iframe.frameMargin=0;
        iframe.framePadding=0;
        iframe.height=200;
        if(textarea.attr('class'))
            iframe.className = textarea.attr('class');
        if(textarea.attr('id'))
            iframe.id = textarea.attr('id');
        if(textarea.attr('name'))
            iframe.title = textarea.attr('name');
        textarea.after(iframe);
        var css = "";
        if(css_url)
            var css = "<link type='text/css' rel='stylesheet' href='"+css_url+"' />";
        var content = textarea.val();
        // Mozilla need this to display caret
        if($.trim(content)=='')
            content = '<br>';
        var doc = "<html><head>"+css+"</head><body class='frameBody'>"+content+"</body></html>";
        tryEnableDesignMode(iframe, doc, function() {
            $("#toolbar-"+iframe.title).remove();
            $(iframe).before(toolbar(iframe));
            textarea.remove();
            iframe.contentWindow.document.execCommand("styleWithCSS", false, false);
            textbox = $('body', $(iframe.contentWindow.document));
        });
    }

    function toolbar(iframe) {

        var tb = $("<div class='rte-toolbar' id='toolbar-"+iframe.title+"'><div>\
            <p>\
                <a href='#' class='tb-button highlight'><i class='fa fa-pencil'></i></a>\
                <a href='#' class='tb-button bold'><i class='fa fa-bold'></i></a>\
                <a href='#' class='tb-button italic'><i class='fa fa-italic'></i></a>\
                <a href='#' class='tb-button orderedlist'><i class='fa fa-list-ol'></i></a>\
                <a href='#' class='tb-button unorderedlist'><i class='fa fa-list-ul'></i></a>\
            </p></div></div>");
        $('.highlight', tb).click(function() {
            formatText(iframe, 'insertHTML', "<span class='keyword'>" + iframe.contentWindow.document.getSelection() + "</span>");
            on_type($('body', iframeDoc));
            return false;
        });
        $('.bold', tb).click(function() {
            formatText(iframe, 'bold');
            return false;
        });
        $('.italic', tb).click(function() {
            formatText(iframe, 'italic');
            return false;
        });
        $('.orderedlist', tb).click(function() {
            formatText(iframe, 'insertorderedlist');
            return false;
        });
        $('.unorderedlist', tb).click(function() {
            formatText(iframe, 'insertunorderedlist');
            return false;
        });
        $(iframe).parents('form').submit(function(){
            disableDesignMode(iframe, true); });
        var iframeDoc = $(iframe.contentWindow.document);

        iframeDoc.keyup(function() {
            on_type();
            var body = $('body', iframeDoc);
            if(body.scrollTop()>0)
                iframe.height = Math.min(350, parseInt(iframe.height)+body.scrollTop());
            return true;
        });

        return tb;
    }
}
