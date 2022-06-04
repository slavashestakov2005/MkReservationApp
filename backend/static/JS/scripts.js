let timer = null;
let xhr = null;


function popover_start(elem){
    timer = null;
    let hr = elem.children()[0].href;
    xhr = $.ajax(hr).done(
        function(data) {
            xhr = null;
            elem.popover({
                trigger: 'manual',
                html: true,
                animation: false,
                container: elem,
                content: data
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
