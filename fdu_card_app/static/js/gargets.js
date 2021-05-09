function getCookieByString(cookieName) {
    var start = document.cookie.indexOf(cookieName + '=');
    if (start == -1) return false;
    start = start + cookieName.length + 1;
    var end = document.cookie.indexOf(';', start);
    if (end == -1) end = document.cookie.length;
    return document.cookie.substring(start, end);
}

function addClassList(element, str) {
    var classList = str.split(" ");
    classList.forEach(classElement => {
        element.classList.add(classElement);
    });
}