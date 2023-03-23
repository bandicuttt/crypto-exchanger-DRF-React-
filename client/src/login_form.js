import './css/styles.css'
import {useContext, useEffect, useRef, useState} from "react";
import FormContext from "./FormContext";

function LoginForm() {
    const formRef = useRef();
    const {form, setForm } = useContext(FormContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [usernameError, setUsernameError] = useState("");
    const [passwordError, setPasswordError] = useState("");
    function HandleClick() {
        setForm(1)
    }
    async function handleSubmit(e) {
        e.preventDefault();

        if (username.trim() === "") {
            setUsernameError("Username is required.");
            return;
        }
        setUsernameError("");

        if (password.trim() === "") {
            setPasswordError("Password is required.");
            return;
        }
        setPasswordError("");
        try {
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
        } catch (error) {
            console.error('Error:', error);
        }
    }
    return (
        <form className={"login-form"} ref={formRef} onSubmit={handleSubmit}>
            <input type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
            {usernameError && <div className="error">{usernameError}</div>}
            <input type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            {passwordError && <div className="error">{passwordError}</div>}
            <button>login</button>
            <p className="message">Not registered? <a href="#" onClick={HandleClick}>Create an account</a></p>
        </form>
    );
}

export default LoginForm;