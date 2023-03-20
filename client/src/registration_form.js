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