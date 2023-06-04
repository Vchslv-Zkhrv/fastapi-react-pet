import React, { useContext, useMemo, useState } from "react";

import { UserContext } from "../context/userContext";
import ErrorMessage from "./ErrorMessage";


const Register = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmationPassword, setConfirmarionPassword] = useState("");
    const [errorMesage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);

    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body:   JSON.stringify({ email: email, hashed_password: password })
        };
        const response = await fetch("/api/users", requestOptions);
        const data = await response.json();

        if (!response.ok) { setErrorMessage(data.detail); }
        else { setToken(data.access_token); }
    }

    const handleSubmit = (e) => {
    
        // check password lenght before regitration the user
        e.preventDefault();
    
        if (password === confirmationPassword && password.length > 5) {
            submitRegistration()
        }
        else {
            setErrorMessage("Password must be greater than 5 characters")
        }
    }

    return (
        <div className="column">
            <form className="box" onSubmit={(e) => handleSubmit(e)}>
                <h1 className="title has-text-centered">Register</h1>
                <div className="field">
                    <label className="label">Email address</label>
                    <div className="control">
                        <input
                            type="text"
                            placeholder="Enter email"
                            onChange={(e) => setEmail(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                            type="password"
                            placeholder="Enter password"
                            onChange={(e) => setPassword(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Confirm password</label>
                    <div className="control">
                        <input
                            type="password"
                            placeholder="Retype password"
                            onChange={(e) => setConfirmarionPassword(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <ErrorMessage message={errorMesage}></ErrorMessage>
                <br />
                <button className="button is-primary" type="Submit">Submit</button>
            </form>
        </div>
    );

}

export default Register;
