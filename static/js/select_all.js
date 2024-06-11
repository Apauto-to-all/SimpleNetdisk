function chk_all() {
    var chkall = document.getElementById('chkall').checked;
    var checkboxes = document.querySelectorAll('input[type=checkbox]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = chkall;
    }
}
function chk_single() {
    var checkboxes = document.querySelectorAll('input[type=checkbox].checkboxItem');
    var allChecked = true;
    var someChecked = false;
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            someChecked = true;
        } else {
            allChecked = false;
        }
    }
    var chkall = document.getElementById('chkall');
    chkall.checked = allChecked;
    chkall.indeterminate = someChecked && !allChecked;
}