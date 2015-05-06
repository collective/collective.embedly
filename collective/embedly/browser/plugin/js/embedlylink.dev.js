/* Functions for the plonelink plugin popup */
/*jslint evil: true */
// tinyMCEPopup.requireLangPack();

function displayTab(tab_id, panel_id) {
    var panelElm, panelContainerElm, tabElm, tabContainerElm, nodes, i;
    tabElm = document.getElementById(tab_id);
    panelElm = document.getElementById(panel_id);
    panelContainerElm = panelElm ? panelElm.parentNode : null;
    tabContainerElm = tabElm ? tabElm.parentNode : null;
    if (tabElm && tabContainerElm) {
        nodes = tabContainerElm.childNodes;
        // Hide all other tabs
        for (i = 0; i < nodes.length; i++) {
            if (nodes[i].nodeName == "LI") {
                nodes[i].getElementsByTagName("a")[0].className = '';
                nodes[i].tabIndex = -1;
            }
        }
        // Show selected tab
        tabElm.getElementsByTagName("a")[0].className = 'selected';
        tabElm.tabIndex = 0;
    }
    if (panelElm && panelContainerElm) {
        nodes = panelContainerElm.childNodes;
        // Hide all other panels
        for (i = 0; i < nodes.length; i++) {
            if (nodes[i].nodeName == "DIV") {
                nodes[i].className = 'panel';
            }
        }
        // Show selected panel
        panelElm.className = 'current';
        toggleYoutubeFields(panelElm);
    }

};

/**
 * hides all fields marked with youtube class
 * in case the url given is not youtube specific
 * (youtube.com or youtu.be)
 *
 * @param {Object} panel
 */
function toggleYoutubeFields(panel){
    if (panel.id != 'advanced_panel') {
        return;
    }
    var url = document.getElementById('externalurl').value;
    var show = false;
    if (url.contains('://youtu') || url.contains('://www.youtu')) {
        show = true;
    }

    function addClass(el, newClassName){
        el.className += ' ' + newClassName;
    }
    function removeClass(el, removeClassName){
        var elClass = el.className;
        while(elClass.indexOf(removeClassName) != -1) {
            elClass = elClass.replace(removeClassName, '');
            elClass = elClass.trim();
        }
        el.className = elClass;
    }

    var nodes = panel.getElementsByTagName("form")[0].getElementsByTagName('div');
    for (i=0; i< nodes.length; i++) {
        var node = nodes[i];
        if (node.className.contains('youtube')) {
            show ? removeClass(node, 'hidden'): addClass(node, 'hidden');
        }
    }
}

var templates = {
    "window.open" : "window.open('${url}','${target}','${options}')"
};

var current_path;
var current_link = "";
var current_url = "";
var current_pageanchor = "";
var labels = "";
var value_getter = ['maxwidth', 'maxheight', 'width', 'callback', 'wmode', 'words', 'chars'];
var checked_getter = ['allowscripts', 'nostyle', 'autoplay', 'videosrc'];
var unchecked_getter = ['youtube_rel'];

function preinit() {
    var url = tinyMCEPopup.getParam("external_link_list_url");

    if (url)
        document.write('<script language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></script>');
}

function initData(href) {
    var hrefsplit = href.split("?");
    if (hrefsplit.length === 2) {
        var paramslist = hrefsplit[1].split("&"), params = {}, eparams = [], newparams = [];
        for (var i in paramslist) {
            var x = paramslist[i].split("=");
            params[x[0]]=x[1];
        }
        for (i in value_getter) {
            if (value_getter[i] in params) {
                document.getElementById(value_getter[i]).value = params[value_getter[i]];
                eparams.push(value_getter[i]);
            }
        }
        for (i in checked_getter) {
            if (checked_getter[i] in params) {
                document.getElementById(checked_getter[i]).checked = true;
                eparams.push(checked_getter[i]);
            }
        }
        for (i in unchecked_getter) {
            if (unchecked_getter[i] in params) {
                var val =  params[unchecked_getter[i]];
                document.getElementById(unchecked_getter[i]).checked = val;
                eparams.push(unchecked_getter[i]);
            }
        }
        for (i in params) {
            if (eparams.indexOf(i)===-1) {
                newparams.push(i+"="+params[i]);
            }
        }
        hrefsplit[1] = newparams.join("&");
        href = hrefsplit.join("?");
    }
    return href;
}

function init() {
    tinyMCEPopup.resizeToInnerSize();

    var formGeneralObj = document.forms[0];
    var formAdvancedObj = document.forms[1];
    var formButtonsObj = document.forms[2];
    var inst = tinyMCEPopup.editor;
    var elm = inst.selection.getNode();
    var action = "insert";
    var html;
    var href;
    labels = eval(inst.getParam('labels'));

    // Check if update or insert
    elm = inst.dom.getParent(elm, "A");
    if (elm !== null && elm.nodeName == "A")
        action = "update";

    // Set button caption
    formButtonsObj.insert.value = 'Insert';

    // Check if rooted
    if (tinyMCEPopup.editor.settings.rooted) {
        document.getElementById('home').style.display = 'none';
    }

    if (action == "update") {
        href = inst.dom.getAttrib(elm, 'href');
        href = tinymce.trim(href);

        // Setup form data
        setFormValue('href', href, 0);
        if ((typeof(elm.title) != "undefined") && (elm.title !== "")) {
            setFormValue('title', inst.dom.getAttrib(elm, 'title'), 2);
        }
        href = initData(href);
        setFormValue('externalurl', href, 0);
    } else {
        href = inst.selection.getContent();
        href = tinymce.trim(href);
        if (href.indexOf('http') === 0) setFormValue('externalurl', href, 0);
    }
}

function getParentUrl(url) {
    var url_array = url.split('/');
    url_array.pop();
    return url_array.join('/');
}

function getAbsoluteUrl(base, link) {
    if ((link.indexOf('http://') != -1) || (link.indexOf('https://') != -1) || (link.indexOf('ftp://') != -1)) {
        return link;
    }

    var base_array = base.split('/');
    var link_array = link.split('/');

    // Remove document from base url
    base_array.pop();

    while (link_array.length !== 0) {
        var item = link_array.shift();
        if (item == ".") {
            // Do nothing
        } else if (item == "..") {
            // Remove leave node from base
            base_array.pop();
        } else {
            // Push node to base_array
            base_array.push(item);
        }
    }
    return (base_array.join('/'));
}

function setFormValue(name, value, formnr) {
    document.forms[formnr].elements[name].value = value;
}

function setAttrib(elm, attrib, value, formnr) {
    var formObj = document.forms[formnr];
    var valueElm = formObj.elements[attrib.toLowerCase()];
    var dom = tinyMCEPopup.editor.dom;

    if (typeof(value) == "undefined" || value === null) {
        value = "";

        if (valueElm)
            value = valueElm.value;
    }

    dom.setAttrib(elm, attrib, value);
}

function previewExternalLink() {
    var url = document.getElementById('externalurl').value;
    elink = "http://api.embed.ly/1/oembed?format=json";
    params = {};
    params.url = escape(url);
    for(var i in params){
      if(params[i])
        elink += '&'+i+'='+params[i];
    }
    var request = window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
    var preview = document.getElementById('previewexternal');
    request.open( "GET", elink, true );
    request.onreadystatechange = function () {
        if ( request.readyState == request.DONE ) {
            if ( request.status == 200 ) {
                var resp = eval( "(" + request.responseText + ")" );
                if(resp.type == 'error'){
                    preview.innerHTML="<p class='error'>We couldn't process this URL. Try again, or email support@embed.ly.</p>";
                } else {
                    if (resp.type === 'photo'){
                        code = '<a href="'+url+'" target="_blank"><img style="width:100%" src="'+resp.url+'" title="'+resp.title||document.title+'" /></a>';
                    } else if (resp.type === 'video'){
                        code = resp.html;
                    } else if (resp.type === 'rich'){
                        code = resp.html;
                    } else {
                        thumb = resp.thumbnail_url ? '<img src="'+resp.thumbnail_url+'" class="thumb embedly-thumbnail-small" />' : '';
                        description = resp.description;
                        code = thumb+"<a class='embedly-title' href='" + url + "'>" + title + "</a>";
                        code += description;
                    }
                    // Wrap the embed in our class for manipulation
                    pr = '<div class="embedly">'+code + '</div>';
                    preview.innerHTML = pr;
                }
            } else {
            preview.innerHTML="<p class='error'>We couldn't process this URL. Try again, or email support@embed.ly.</p>";
            }
            request = null;
        }
    };
    request.send();
}

function getInputValue(name, formnr) {
    return document.forms[formnr].elements[name].value;
}

function buildHref() {
    var href = "", params = [], name, title, i, value;
    var inst = tinyMCEPopup.editor;

    href = document.getElementById('externalurl').value;
    for (i in value_getter) {
        value = document.getElementById(value_getter[i]).value;
        if (value !== '') params[value_getter[i]] = value;
    }
    for (i in checked_getter) {
        value = document.getElementById(checked_getter[i]).checked;
        if (value) params[checked_getter[i]] = 'true';
    }

    for (i in unchecked_getter) {
        value = document.getElementById(unchecked_getter[i]).checked;
        if (value) params[unchecked_getter[i]] = 'false';
    }
    for (i in params) {
        if (href.indexOf("?") === -1) {
            href+="?";
        } else {
            href+="&";
        }
        href+=i+"="+params[i];
    }
    document.forms[0].href.value = href;
}

function insertAction() {
    var inst = tinyMCEPopup.editor;
    var elm, elementArray, i;

    buildHref();
    elm = inst.selection.getNode();
    elm = inst.dom.getParent(elm, "A");

    // Remove element if there is no href
    if (!document.forms[0].href.value) {
        tinyMCEPopup.execCommand("mceBeginUndoLevel");
        i = inst.selection.getBookmark();
        inst.dom.remove(elm, 1);
        inst.selection.moveToBookmark(i);
        tinyMCEPopup.execCommand("mceEndUndoLevel");
        tinyMCEPopup.close();
        return;
    }

    tinyMCEPopup.execCommand("mceBeginUndoLevel");

    // Create new anchor elements
    if (elm === null) {
        inst.getDoc().execCommand("unlink", false, null);
        tinyMCEPopup.execCommand("CreateLink", false, "#mce_temp_url#", {skip_undo : 1});

        elementArray = tinymce.grep(inst.dom.select("a"), function(n) {return inst.dom.getAttrib(n, 'href') == '#mce_temp_url#';});
        for (i=0; i<elementArray.length; i++)
            setAllAttribs(elm = elementArray[i]);
    } else
        setAllAttribs(elm);

    // Don't move caret if selection was image
    if (elm && (elm.childNodes.length != 1 || elm.firstChild.nodeName != 'IMG')) {
        inst.focus();
        inst.selection.select(elm);
        inst.selection.collapse(0);
        tinyMCEPopup.storeSelection();
    }

    tinyMCEPopup.execCommand("mceEndUndoLevel");
    tinyMCEPopup.close();
}

function setAllAttribs(elm) {
    var formGeneralObj = document.forms[0];
    var formAdvancedObj = document.forms[1];
    var formButtonsObj = document.forms[2];

    var href = formGeneralObj.href.value;
    setAttrib(elm, 'href', href, 0);
    setAttrib(elm, 'title', formAdvancedObj.title.value, 2);

    var dom = tinyMCEPopup.editor.dom;
    dom.addClass(elm, 'embedlylink');

    // Refresh in old MSIE
    if (tinyMCE.isMSIE5)
        elm.outerHTML = elm.outerHTML;
}

function getSelectValue(form_obj, field_name) {
    var elm = form_obj.elements[field_name];

    if (!elm || elm.options === null || elm.selectedIndex == -1)
        return "";

    return elm.options[elm.selectedIndex].value;
}

// While loading
preinit();
tinyMCEPopup.onInit.add(init);

