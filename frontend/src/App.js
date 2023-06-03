import React, { useEffect, useState } from "react";

const App = () => {

    const [message, setMessage] = useState("");

    //  check the connection to backend server when app is started

    const getWelcomeMessage = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "Application/json"
            },
        };
        const response = await fetch("/api", requestOptions);
        
        if (!response.ok) {
            console.log("no connection to server")
        }
        else {
            response.json().then(data => setMessage(data["message"]))
        }
    }

    useEffect(() => {
        getWelcomeMessage();
    }, [])

  return (
    <div>
        <h1>{message}</h1>
    </div>
  );
}

export default App;
