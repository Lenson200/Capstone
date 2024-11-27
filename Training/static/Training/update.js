document.addEventListener('DOMContentLoaded', () => {
    const showFormButton = document.getElementById('show-form-button');
    const profileForm = document.querySelector('.profileform');
    const loginForm = document.querySelector('#login-form'); 

    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent the default form submission
            const formData = new FormData(loginForm);
            fetch('/login?next=/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', 
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('login-message');
                messageDiv.innerHTML = `
                          <div class="login-message">
                            <strong>Success!</strong><br>
                            <p>Login successful. Welcome!</p>
                            <button class="close-btn" onclick="this.parentElement.remove()">×</button> <!-- Close button -->
                        </div>`; 
                // Append the message div to the body or any other element on the page
                document.body.appendChild(messageDiv);
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 3000);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error during login:', error);
            });
        });
    }
    
    showFormButton.addEventListener('click', () => {
        showFormButton.style.display = 'none'; // Hide the button
        profileForm.style.display = 'block';  // Show the form
    });

    // Hide form and show button after form submission
    profileForm.addEventListener('submit', () => {
        setTimeout(() => {
            profileForm.style.display = 'none'; // Hide the form
            showFormButton.style.display = 'block'; // Show the button
        }, 100); // Adjust timing if needed
    });

});