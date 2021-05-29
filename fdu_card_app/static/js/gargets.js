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

function showTable(tableId, data) {
    htmlKit = {
        _tags: [], html: [],
        _createAttrs: function (attrs) {
            var attrStr = [];
            for (var key in attrs) {
                if (!attrs.hasOwnProperty(key)) continue;
                attrStr.push(key + "=" + attrs[key] + "")
            }
            return attrStr.join(" ")
        }, _createTag: function (tag, attrs, isStart) {
            if (isStart) {
                return "<" + tag + " " + this._createAttrs(attrs) + ">"
            } else {
                return "</" + tag + ">"
            }
        }, start: function (tag, attrs) {
            this._tags.push(tag);
            this.html.push(this._createTag(tag, attrs, true));
            return this;
        }, end: function () {
            this.html.push(this._createTag(this._tags.pop(), null, false));
            return this;
        }, tag: function (tag, attr, text) {
            this.html.push(this._createTag(tag, attr, true) + text + this._createTag(tag, null, false));
            return this;
        },
        create: function () {
            var t = this.html.join("");
            this.clear();
            return t;
        },
        clear: function () {
            this._tags = [];
            this.html = [];
        }
    };

    function json2Html(data) {
        var hk = htmlKit;
        hk.start("table", { "cellpadding": "10", "border": "1" });
        hk.start("thead");
        hk.start("tr");
        data["heads"].forEach(function (head) {
            hk.tag("th", { "bgcolor": "AntiqueWhite" }, head)
        });
        hk.end();
        hk.end();
        hk.start("tbody");
        data["data"].forEach(function (dataList, i) {
            dataList.forEach(function (_data) {
                hk.start("tr");
                data["dataKeys"][i].forEach(function (key) {
                    var rowsAndCol = key.split(":");
                    if (rowsAndCol.length === 1) {
                        hk.tag("td", null, _data[rowsAndCol[0]])
                    } else if (rowsAndCol.length === 3) {
                        hk.tag("td", { "rowspan": rowsAndCol[0], "colspan": rowsAndCol[1] }, _data[rowsAndCol[2]])
                    }
                });
                hk.end()
            })
        });
        hk.end();
        hk.end();
        return hk.create()
    }

    var tableHTML = json2Html(data);
    var table = document.getElementById(tableId);
    table.innerHTML = tableHTML;
}

jQuery.fn.onPositionChanged = function (trigger, millis) {
    if (millis == null) millis = 100;
    var o = $(this[0]); // our jquery object
    if (o.length < 1) return o;

    var lastPos = null;
    var lastOff = null;
    setInterval(function () {
        if (o == null || o.length < 1) return o; // abort if element is non existend eny more
        if (lastPos == null) lastPos = o.position();
        if (lastOff == null) lastOff = o.offset();
        var newPos = o.position();
        var newOff = o.offset();
        if (lastPos.top != newPos.top || lastPos.left != newPos.left) {
            $(this).trigger('onPositionChanged', { lastPos: lastPos, newPos: newPos });
            if (typeof (trigger) == "function") trigger(lastPos, newPos);
            lastPos = o.position();
        }
        if (lastOff.top != newOff.top || lastOff.left != newOff.left) {
            $(this).trigger('onOffsetChanged', { lastOff: lastOff, newOff: newOff });
            if (typeof (trigger) == "function") trigger(lastOff, newOff);
            lastOff = o.offset();
        }
    }, millis);

    return o;
};
function fitWindow() {
    var section_header_rec = $(".section-header")[0].getBoundingClientRect();
    var sidebar_wrapper_rec = $("#sidebar-wrapper")[0].getBoundingClientRect();
    var body = $('body')
    if (section_header_rec.left <= sidebar_wrapper_rec.right) {
        body.removeClass('sidebar-show');
        body.addClass('sidebar-mini');
    }
}