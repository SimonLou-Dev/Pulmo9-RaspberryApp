import {useEffect, useState} from 'react'


import {eel} from './eel.js';
import {Route, Routes} from "react-router-dom"

import {Layout} from "./Views/Layout.jsx";
import UserContext from "./components/Context/UserContext.jsx";
import {Login} from "./Views/Auth/Login.jsx";
import {Register} from "./Views/Auth/Register.jsx";
import {PatientList} from "./Views/Patient/PatientList.jsx";
import {NoMatchRoute} from "./components/Utils/NoMatchRoute.jsx";


function App() {
    const [user, setUser] = useState(null)
    const [count, setCount] = useState(0)

    useEffect(() => {
        eel.set_host("ws://localhost:8888");

        return () => {

        }
    }, []);

    return (

            <UserContext.Provider value={{user: user, setUser: (v) => setUser(v)}}>
                <Routes>
                    <Route path="/login" element={<Login/>}/>
                    <Route path={"/register"} element={<Register/>}/>

                    <Route path={"/"}  element={<Layout />}>
                        <Route path={"patients"} element={<PatientList/>}/>
                        <Route index element={<NoMatchRoute/>} />
                    </Route>
                </Routes>
            </UserContext.Provider>
    )
}

export default App;
