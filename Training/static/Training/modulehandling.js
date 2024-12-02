document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-status-btn');

    

    if (toggleButton) {
        const trainingModuleId = toggleButton.getAttribute('data-id');

        // Fetch the current status of the training module when the page loads
        fetch(`/get-training-status/${trainingModuleId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const currentStatus = data.read_status;  
                    toggleButton.textContent = currentStatus ? 'Mark as Unread' : 'Mark as Read';
                    toggleButton.setAttribute('data-status', currentStatus.toString()); 
                } else {
                    console.error('Error fetching current status');
                }
            })
            .catch(error => {
                console.error('Error fetching training status:', error);
            });

        toggleButton.addEventListener('click', async function(event) {
            const currentStatus = toggleButton.getAttribute('data-status') === 'true'; 
            const newStatus = !currentStatus;  

            // Send a POST request to toggle the status
            try {
                const response = await fetch('/toggle-training-status/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        training_module_id: trainingModuleId,
                        read_status: newStatus,
                    }),
                });

                const data = await response.json();
                if (data.success) {
                    toggleButton.textContent = newStatus ? 'Mark as Unread' : 'Mark as Read';
                    toggleButton.setAttribute('data-status', newStatus.toString());  
                } else {
                    alert('Error toggling status.');
                }
            } catch (error) {
                console.error('Error toggling training module status:', error);
            }
        });
    }
});

function getCookie(name) {
    const cookieValue = document.cookie.match(`(^|;)\\s*${name}=([^;]+)`);
    return cookieValue ? cookieValue.pop() : '';
}
