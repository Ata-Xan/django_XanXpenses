const usernameField = document.querySelector('#username');
const usernamefeedbackArea = document.querySelector('.usernameFeedBackArea');

const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput")
const submitBtn = document.querySelector(".submit-btn")
usernameField.addEventListener("keyup", (e) => {
    const usernameValue = e.target.value;
    usernamefeedbackArea.classList.remove('is-invalid');
    usernameSuccessOutput.textContent = `Checking ${usernameValue}`;
    usernamefeedbackArea.style.display = "none";

    if (usernameValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data)
                usernameSuccessOutput.style.display = 'none';
                if (data.username_error) {
                    usernameField.classList.add('is-invalid');
                    submitBtn.setAttribute('disabled', 'true');
                    usernamefeedbackArea.style.display = "block";
                    usernamefeedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                    console.log("the btn should be disabled.")
                } else {
                    submitBtn.removeAttribute('disabled');
                    console.log('Before removing is-invalid class:', usernameField.classList);
                    usernameField.classList.remove('is-invalid');
                    console.log('After removing is-invalid class:', usernameField.classList);
                }
            })
    }
});

const emailInput = document.querySelector('#email');
const emailFeedbackArea = document.querySelector('.emailFeedBackArea');
emailInput.addEventListener('input', function () {
    const email = emailInput.value;
    // console.log(email);
    const xhr = new XMLHttpRequest();
    // emailFeedbackArea.style.display="none";
    xhr.open('POST', "validate-email");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {

        const response = JSON.parse(xhr.responseText);
        if (response.valid) {
            // emailInput.setCustomValidity('');
            emailFeedbackArea.style.display = "none";
            emailInput.classList.remove("is-invalid");
            submitBtn.removeAttribute('disabled');

        } else {
            emailFeedbackArea.style.display = "block";
            emailInput.classList.add("is-invalid");
            submitBtn.setAttribute('disabled', 'true');
            emailFeedbackArea.innerHTML = `<p>Please enter a valid  email address.</p>`;
            console.log("the btn should be disabled.")
            // emailInput.setCustomValidity('Please enter a valid email address.');

        }
    };
    xhr.send('email=' + encodeURIComponent(email))
    // console.log(xhr)
});

const passwordInput = document.getElementById('password');
const showPasswordToggle = document.getElementById('show-password-toggle');

showPasswordToggle.addEventListener('click', function () {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
    // toggle eye icon
    const eyeIcon = showPasswordToggle.querySelector('i');
    if (eyeIcon.classList.contains('fa-eye')) {
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
});


// code for checking if the FontAwesome is working fine
// window.onload = function () {
//     var span = document.createElement('span');
//
//     span.className = 'fa';
//     span.style.display = 'none';
//     document.body.insertBefore(span, document.body.firstChild);
//
//     alert(window.getComputedStyle(span, null).getPropertyValue('font-family'));
//
//     document.body.removeChild(span);
// };

