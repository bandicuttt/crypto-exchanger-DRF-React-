import './css/styles.css'
import RegistrationForm from "./registration_form";
import LoginForm from "./login_form";
import {useEffect, useRef, useState} from "react";
import FormContext from "./FormContext";


function AuthPage() {
    const [form, setForm] = useState(1);
    return (
        <FormContext.Provider value={{ form, setForm}}>
            <div className={"login-page"}>
            <div className={"form"}>
                {form === 1 ? <RegistrationForm/> : <LoginForm/>}
            </div>
          </div>
        </FormContext.Provider>
    );
  }
  
  export default AuthPage;