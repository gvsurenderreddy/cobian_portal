function getCookie(c_name)
{
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++)
    {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name)
        {
            return unescape(y);
        }
    }
}

function setCookie(c_name, value, exdays)
{
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays==null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}

window.showLoadingTimer = function(){};
function showLoading($el, nobg) {
    clearTimeout(showLoadingTimer);
    window.showLoadingTimer = setTimeout(function() {
        $('#loading_overlay, #loading_dim').remove();
        $el = $el || $('body');
        var top = $el.offset().top,
            left = $el.offset().left,
            width = $el.outerWidth(),
            height = $el.outerHeight(),
            xpos = left+(width/2)-75,
            ypos = top + (height/2)-10;

        var dim = $('<div id="loading_dim"></div>');
        dim.css('width', width).css('height', $el[0].scrollHeight).css('background', function(){if (nobg) return ''; else return '#d8d8d8'}).css('opacity', '.3')
            .css('position', 'absolute').css('left', left).css('top', top).css('border-radius', $el.css('border-radius'));
        $el.after(dim);
        
        loadingEl = $('<div id="loading_overlay"><div class="progress progress-striped active"><div class="progress-bar"  role="progressbar" style="width:100%;background-color:#d8d8d8"><span style="line-height:19px">Loading...</span></div></div></div>');
        loadingEl.css('width', '150px').css('height', '20px').css('text-align', 'center').css('vertical-align', 'middle').css('z-index', '9999')
            .css('position', 'absolute').css('left', xpos+'px').css('top', ypos+'px');
        $el.after(loadingEl);

    }, 500);
}

function hideLoading() {
    clearTimeout(showLoadingTimer);
    $('#loading_overlay, #loading_dim').remove();
}
