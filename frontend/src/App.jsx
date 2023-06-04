import React, { useContext, useEffect, useState } from "react";
import Register from "./components/Register";
import Header from "./components/Header";
import { UserContext } from "./context/userContext";
import Login from "./components/Login";

const App = () => {

    //  check the connection to backend server when app is started

    const [message, setMessage] = useState("");
    const [token, setToken] = useContext(UserContext)

    const getWelcomeMessage = async () => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "Application/json"}
        };
        const response = await fetch("/api", requestOptions);
        
        if (!response.ok) { setMessage("no connection to server") }
    }

    useEffect(() => {
        getWelcomeMessage();
    }, [])

  return (
    <div>
        <Header title={message} />
        <div className="columns">
            <div className="column"></div>
            <div className="column m-5 is-two-thirds">
                {!token
                    ? (
                        <div className="columns">
                            <Register/> <Login/>
                        </div>
                    )
                    : (
                        <p>Table</p>
                    )
                }
            </div>
            <div className="column"></div>
        </div>
    </div>
  );
}

export default App;
