import {useEffect, useState} from 'react'
import {Route, Routes} from "react-router-dom"

import {Layout} from "./Views/Layout.jsx";
import UserContext from "./components/Context/UserContext.jsx";
import {Login} from "./Views/Auth/Login.jsx";
import {Register} from "./Views/Auth/Register.jsx";
import {PatientList} from "./Views/Patient/PatientList.jsx";
import {NoMatchRoute} from "./components/Utils/NoMatchRoute.jsx";
import {WaitAuth} from "./Views/WaitAuth.jsx";
import {myEel} from "./MyEel.js";


/* Custom socket events */
const blHasTimeout = new CustomEvent('blTimeout', { detail: { message: 'Bluetooth connection timeout' } });
const blIsConnected = new CustomEvent('blConnected', { detail: { message: 'Bluetooth connection established' } });


function App() {
    const [user, setUser] = useState(null)
    const [blConnected, setBlConnected] = useState(false)

    useEffect(() => {
        myEel.set_host("ws://localhost:8888");

        const interval = setInterval(handleBl, 2000);

        window.addEventListener("unload", (event) => {
            myEel.sendClose()();
        });

        return () => {
            clearInterval(interval);
        }

    }, []);

    const handleBl = async () => {
        await myEel.get_socket_status()().then((r) => {
            if(blConnected && !r.connected){
                setBlConnected(false);
            }else if(!blConnected && r.connected){
                setBlConnected(true);
            }

            if(r.timedOut){
                setBlConnected(false)
            }

        });

        //window.dispatchEvent(blConnected)
    }

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
