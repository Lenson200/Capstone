document.addEventListener('DOMContentLoaded', () => {
    const showFormButton = document.getElementById('show-form-button');
    const profileForm = document.querySelector('.profileform');
    const loginForm = document.querySelector('#login-form');
  
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevents the default form submission
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
                // Appends the message div to the body or any other element on the page
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
        showFormButton.style.display = 'none'; 
        profileForm.style.display = 'block'; 
    });
    
    // Hide form and show button after form submission
    profileForm.addEventListener('submit', () => {
        setTimeout(() => {
            profileForm.style.display = 'none'; 
            showFormButton.style.display = 'block'; 
        }, 100);
    });
    
   


   
});
   

// const submitButton = document.getElementById('submit-button');
// const trainingModuleId = document.getElementById('training_module_id').value;
// const messageDiv = document.getElementById('message');
// const toggleTrainingStatus = () => {
//     fetch(`toggle-training-status/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             training_module_id: trainingModuleId,
//         }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             // Update button text based on new status
//             submitButton.textContent = data.is_completed
//                 ? 'Mark Module Incomplete'
//                 : 'Mark Module Complete';

//             // Show success message
//             messageDiv.textContent = data.message;
//             messageDiv.style.display = 'block';
//             messageDiv.style.color = 'green';
//         } else {
//             // Show error message
//             messageDiv.textContent = data.message;
//             messageDiv.style.display = 'block';
//             messageDiv.style.color = 'red';
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         messageDiv.textContent = 'An error occurred. Please try again.';
//         messageDiv.style.display = 'block';
//         messageDiv.style.color = 'red';
//     });
// };

// // Add click event listener to the button
// submitButton.addEventListener('click', toggleTrainingStatus);