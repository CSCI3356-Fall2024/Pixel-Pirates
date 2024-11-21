// Show popup
function showPopup(taskId) {
    document.getElementById(`popup-${taskId}`).style.display = "block";
    document.getElementById(`overlay-${taskId}`).style.display = "block";
}

// Hide popup
function hidePopup(taskId) {
    document.getElementById(`popup-${taskId}`).style.display = "none";
    document.getElementById(`overlay-${taskId}`).style.display = "none";
}

// Mark task as completed
function markTaskCompleted(taskId, checkbox) {
    if (checkbox.checked) {
        fetch(`/tasks/complete/${taskId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close the popup
                hidePopup(taskId);

                // Refresh the page after task completion
                location.reload();
            } else {
                alert(data.error || "Failed to mark task as completed.");
                checkbox.checked = false;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            checkbox.checked = false;
        });
    }
}

// Get CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return null;
}

