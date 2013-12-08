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
        iframe.height = document.documentElement.clientHeight - 250 + "px";
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

        var tb = $("<div class='rte-toolbar' id='toolbar-"+iframe.title+"'>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button highlight'><i class='fa fa-pencil'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button bold'><i class='fa fa-bold'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button italic'><i class='fa fa-italic'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button underline'><i class='fa fa-underline'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button strikethrough'><i class='fa fa-strikethrough'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button subscript'><i class='fa fa-subscript'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button superscript'><i class='fa fa-superscript'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button orderedlist'><i class='fa fa-list-ol'></i></a>&nbsp;</div>\
            <div class='tb-button-box'><a href='javascript:void(0);' class='tb-button unorderedlist'><i class='fa fa-list-ul'></i></a>&nbsp;</div>\
            <div class='tb-button-box'>\
                <a href='javascript:void(0);' class='tb-button options'><i class='fa fa-cog'></i></a>\
                <div id='tb-menu'>\
                    <a href='/download/"+docid+"/txt' class='tb-menu-item' download='document_"+docid+".txt'><i class='fa fa-download'></i>&nbsp;&nbsp;Download as TXT</a>\
                    <a href='/download/"+docid+"/pdf' class='tb-menu-item' download='document_"+docid+".pdf'><i class='fa fa-download'></i>&nbsp;&nbsp;Download as PDF</a>\
                    <a href='javascript:void(0);' class='tb-menu-item' id='tb-menu-delete'><i class='fa fa-times-circle'></i>&nbsp;&nbsp;Delete</a>\
                </div>\
            </div>\
            <div class='tb-status-box'><p>\
                <span id='tb-status-text'>Loading</span>&nbsp;<i id='tb-status' class='fa fa-exclamation-circle'></i>\
            </p></div></div>");
        $('.highlight', tb).click(function() {
            formatText(iframe, 'insertHTML', "<span class='keyword'>" + iframe.contentWindow.document.getSelection() + "</span>");
            on_type();
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
        $('.underline', tb).click(function() {
            formatText(iframe, 'underline');
            return false;
        });
        $('.strikethrough', tb).click(function() {
            formatText(iframe, 'strikethrough');
            return false;
        });
        $('.subscript', tb).click(function() {
            formatText(iframe, 'subscript');
            return false;
        });
        $('.superscript', tb).click(function() {
            formatText(iframe, 'superscript');
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
        $('.options', tb).click(function() {
            $("#tb-menu").toggle();
            return false;
        });
        $("#tb-menu", tb).hide();
        $(".tb-menu-item", tb).click(function() {
            $("#tb-menu").hide();
        });
        $("#tb-menu-delete", tb).click(function() {
            $("#deleteModal").modal("show")
        });
        $(iframe).parents('form').submit(function(){
            disableDesignMode(iframe, true);
        });
        $(iframe.contentWindow.document).keyup(on_type);
        return tb;
    }
}
