/* hrefs */
function go(url){
    document.location.href = url;
}

function clickCard(card, year=0){
    go((year ? '../' + year + '/' : '') + card + '.html')
}


/* textarea */
function textAreaInput(textarea){
    textarea.style.height = '1px';
    textarea.style.height = (textarea.scrollHeight + 6) + 'px';
}

function initTextArea(){
    let areas = document.getElementsByClassName('js-textarea');
    for (let textarea of areas){
        textarea.oninput = function(){ textAreaInput(textarea); };
        textAreaInput(textarea);
    }
}


/* slider */
function initSlider(){
    document.addEventListener('DOMContentLoaded', () => {
        new ItcSimpleSlider('.itcss', {
            loop: true,
            autoplay: true,
            interval: 5000,
            swipe: true,
        });
    });
}


/* checkbox */
function checkBoxClick(box){
    let children = box.children();
    let chb = $(children[0]).children()[0];
    if (chb.checked){
        children[1].style.display = 'block';
        children[2].style.display = 'none';
    } else{
        children[1].style.display = 'none';
        children[2].style.display = 'block';
    }
}

function initCheckbox(){
    let boxes = document.getElementsByClassName('js-checkbox');
    for(let box of boxes){
        box = $(box);
        $(box.children()[0]).children()[0].onclick = function(){ checkBoxClick(box); };
        checkBoxClick(box);
    }
}


/* markdown */
function convert(str) {
    str = str.replace(/&amp;/g, "&");
    str = str.replace(/&gt;/g, ">");
    str = str.replace(/&lt;/g, "<");
    str = str.replace(/&quot;/g, '"');
    str = str.replace(/&#039;/g, "'");
    return str;
}

function initMDContent() {
    let mds = document.getElementsByClassName('js-md-content');
    for(let md of mds) md.innerHTML = convert(md.innerHTML.toString());
}


/* places color */
function getPlacesColor(value){
    if (value === 0) return 'places-ended';
    else if (value <= 5) return 'places-few';
    else return 'places-many';
}

function setPlacesColor(value){
    let elements = document.getElementsByClassName('places-choice');
    let name = getPlacesColor(value);
    for (let elem of elements) elem.className = 'course-info ' + name;
}


/* markdown simple popover */
let timer = null, xhr = null;

function MDPopoverStart(elem){
    timer = null;
    let hr = elem.children()[0].href;
    let template = elem.children()[1].innerHTML, content_color = ' class="_">';
    xhr = $.ajax(hr).done(
        function(data) {
            xhr = null;
            content_color = content_color.replace('_',  getPlacesColor(data['value']));
            if (data['closing']) template = template.replace('><!-- put is_closing -->', 'class="invisible">');
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

function MDPopoverClear(){
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

function MDPopoverEnd(event){
    let elem = $(event.currentTarget);
    if (!MDPopoverClear()) elem.popover('hide');
}

function initMDPopover(){
    $('.js-md-popover').hover(
        function(event) {
            timer = setTimeout(MDPopoverStart, 1000, $(event.currentTarget));
        }, MDPopoverEnd
    );
    $('.js-md-popover').click(
        function(event) {
            event.preventDefault();
            MDPopoverStart($(event.currentTarget));
        }
    );
    document.addEventListener('click', function(e) {
        MDPopoverClear();
        $('.js-md-popover').popover('hide');
    });
}


/* markdown double click popover */
function MDDoubleClickPopover(md) {
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

function initMDDoubleClickPopover() {
    let mds = document.getElementsByClassName('js-md-double-click-popover');
    for(let md of mds) md.onclick = function(){ MDDoubleClickPopover(md); };
}
