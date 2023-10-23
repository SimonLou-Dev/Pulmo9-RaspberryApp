import {useEffect, useState} from 'react'


import {eel} from './eel.js';
import {Route, Routes} from "react-router-dom"

import {Layout} from "./Views/Layout.jsx";
import UserContext from "./components/Context/UserContext.jsx";
import {Login} from "./Views/Auth/Login.jsx";
import {Register} from "./Views/Auth/Register.jsx";
import {PatientList} from "./Views/Patient/PatientList.jsx";
import {NoMatchRoute} from "./components/Utils/NoMatchRoute.jsx";
import {WaitAuth} from "./Views/WaitAuth.jsx";


function App() {
    const [user, setUser] = useState(null)
    const [blConnected, setBlConnected] = useState(false)

    useEffect(() => {
        eel.set_host("ws://localhost:8888");

        window.addEventListener("unload", (event) => {
            eel.sendClose()();
        });

        window.addEventListener("blTimeout", (event) => {
          setBlConnected(false)
        })

        window.addEventListener("blConnected", (event) => {
            setBlConnected(false)
        })


    }, []);

    return (

            <UserContext.Provider value={{user: user, setUser: (v) => setUser(v), blConnected:blConnected}}>
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path={"/register"} element={<Register/>}/>
                    <Route index element={<WaitAuth/>} />
                    <Route path={"/"}  element={<Layout />}>
                        <Route path={"patients"} element={<PatientList/>}/>

                    </Route>
                </Routes>
            </UserContext.Provider>
    )
}

export default App;
