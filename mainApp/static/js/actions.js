function showPopup(taskId) {
    document.getElementById("popup-" + taskId).style.display = "block";
    document.getElementById("overlay-" + taskId).style.display = "block";
}

function hidePopup(taskId) {
    document.getElementById("popup-" + taskId).style.display = "none";
    document.getElementById("overlay-" + taskId).style.display = "none";
}