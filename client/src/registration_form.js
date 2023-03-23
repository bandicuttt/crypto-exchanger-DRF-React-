import './css/styles.css'
import {useContext, useEffect, useRef, useState} from "react";
import FormContext from "./FormContext";

function RegistrationForm() {
    const formRef = useRef();
    const {form, setForm } = useContext(FormContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [passwordError, setPasswordError] = useState("");
    const [emailError, setEmailError] = useState("");
    const [usernameError, setUsernameError] = useState("");
    function registerUser(username, email, password) {
        const registrationUrl = `${process.env.REACT_APP_API_URL}/api/user/registration/`;
        const registrationData = {
            username: username,
            email: email,
            password: password
        };
        fetch(registrationUrl, {
            method: 'POST',
            body: JSON.stringify(registrationData),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                const tokenUrl = `${process.env.REACT_APP_API_URL}/api/auth/jwt/create/`;
                const tokenData = {
                    username: username,
                    password: password
                };

                fetch(tokenUrl, {
                    method: 'POST',
                    body: JSON.stringify(tokenData),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => {
                            response.json().then(data => {
                                if (data.messageType === 5 && data.message.messageText === "SuccessInfo") {
                                    console.log(data.message.responseBody)
                                    document.cookie = `access_token=${data.message.responseBody.access}`;
                                    document.cookie = `refresh_token=${data.message.responseBody.refresh}`;
                                    const nextPageUrl = '/';
                                    window.location.replace(nextPageUrl);
                                }
                            })




                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    function HandleClick() {
        setForm(2)
    }
    function validatePassword(password) {
        const passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?!.*\s).{8,}$/;
        return passwordRegex.test(password);
    }
    function handleSubmit(e) {
        e.preventDefault();
        if (username.trim() === "") {
            setUsernameError("Username is required.");
            return;
        }
        setUsernameError("");
        if (validatePassword(password)) {
            setPasswordError('')
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                setEmailError("Invalid email format.");
                return;
            }
            registerUser(username, email, password);
            setEmailError("");
        } else {
            setPasswordError("Password must be at least 8 characters long, contain at least 1 digit, at least 1 uppercase letter, and contain no spaces.");
        }
    }
    return (
        <form className={"register-form"} ref={formRef} onSubmit={handleSubmit}>
            <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            {usernameError && <div className="error">{usernameError}</div>}
            <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            {passwordError && <div className="error">{passwordError}</div>}
            <input type="text" placeholder="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            {emailError && <div className="error">{emailError}</div>}
            <button>create</button>
            <p className="message">Already registered? <a  href="#" onClick={HandleClick}>Sign In</a></p>
        </form>
    );
}

export default RegistrationForm;