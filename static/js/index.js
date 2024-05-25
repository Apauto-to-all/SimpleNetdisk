function showUploadForm() {
    var modal = document.getElementById('myModal');
    modal.style.display = "block";
}

window.onload = function () {
    var modal = document.getElementById('myModal');
    var span = document.getElementsByClassName("close")[0];

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}