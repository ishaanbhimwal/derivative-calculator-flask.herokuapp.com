function AvoidSpace(event) {
    var k = event ? event.which : window.event.keyCode;
    if (k == 32) return false;
}

function validateForm() {
    var x = document.forms['myForm']['input'].value;
    if (x == '' || x == null) {
        return false;
    }
}

MathJax = {
    loader: {
        load: ['input/asciimath', 'output/chtml', 'ui/menu']
    },
};

$(document).ready(function () {
    function insertInto(str, input) {
        var val = input.value, s = input.selectionStart, e = input.selectionEnd;
        input.value = val.slice(0, e) + str + val.slice(e);
        if (e == s) input.selectionStart += str.length - 1;
        input.selectionEnd = e + str.length - 1;
    }
    $("input").keypress(function (e) {
        var closures = { 40: ')' };
        if (c = closures[e.which]) insertInto(c, this);
    });
});