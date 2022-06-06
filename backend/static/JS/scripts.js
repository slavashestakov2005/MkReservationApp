let timer = null;
let xhr = null;


function popover_start(elem){
    timer = null;
    let hr = elem.children()[0].href;
    let template = elem.children()[1].innerHTML, content_color = ' class="_">';
    xhr = $.ajax(hr).done(
        function(data) {
            xhr = null;
            if (data['value'] === 0) content_color = content_color.replace('_', 'places-ended');
            else if (data['value'] <= 5) content_color = content_color.replace('_', 'places-few');
            else content_color = content_color.replace('_', 'places-many');
            elem.popover({
                trigger: 'manual',
                html: true,
                animation: false,
                container: elem,
                content: template.replace('><!-- put color of places here -->', content_color).replace('<!-- put empty places here -->', data['value'])
            }).popover('show');
        }
    );
}

function popover_clear(){
    let cls = false;
    if (timer) {
        clearTimeout(timer);
        timer = null;
        cls = true;
    }
    if (xhr) {
        xhr.abort();
        xhr = null;
        cls = true;
    }
    return cls;
}

function popover_end(event){
    let elem = $(event.currentTarget);
    if (!popover_clear()) elem.popover('hide');
}

function popovers(){
    $('.event_popup').hover(
        function(event) {
            timer = setTimeout(popover_start, 1000, $(event.currentTarget));
        }, popover_end
    );
    $('.event_popup').click(
        function(event) {
            event.preventDefault();
            popover_start($(event.currentTarget));
        }
    );
    document.addEventListener('click', function(e) {
        popover_clear();
        $('.event_popup').popover('hide');
    });
}

function textInput(document, textarea){
    textarea.style.height = '1px';
    textarea.style.height = (textarea.scrollHeight + 6) + 'px';
}

function listenInput(document){
    let areas = document.getElementsByClassName('textarea');
    for (let textarea of areas){
        textarea.oninput = function(){ textInput(document, textarea); };
        textInput(document, textarea);
    }
}

function clickCard(document, card, year=0){
    if (year) document.location.href = '../' + year + '/' + card + '.html';
    else document.location.href = card + '.html';
}

function convert(str) {
    str = str.replace(/&amp;/g, "&");
    str = str.replace(/&gt;/g, ">");
    str = str.replace(/&lt;/g, "<");
    str = str.replace(/&quot;/g, '"');
    str = str.replace(/&#039;/g, "'");
    return str;
}

function parseMD(document) {
    let mds = document.getElementsByClassName('markdown-popup');
    for(let md of mds) md.innerHTML = convert(md.innerHTML.toString());
}

function markdown_popover(md) {
    let clickedTime = new Date().getTime();
    let elem = $(md);
    if (elem.children().length === 3){
        elem.popover('hide');
        md.lastClickTime = clickedTime;
        return;
    }
    if (typeof md.lastClickTime === "undefined" || clickedTime - md.lastClickTime > 1000){
        md.lastClickTime = clickedTime;
        return;
    }
    md.lastClickTime = clickedTime;
    let data = convert(elem.children()[1].innerHTML.toString());
    elem.popover({
        trigger: 'manual',
        html: true,
        animation: true,
        container: elem,
        content: data
    }).popover('show');
}

function showMD(document) {
    let mds = document.getElementsByClassName('markdown-text');
    for(let md of mds) md.onclick = function(){ markdown_popover(md); };
}

function visit(document, url) {
    document.location.href = url;
}
