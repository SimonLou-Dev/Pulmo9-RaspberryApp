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
import {PatientEditor} from "./Views/Patient/PatientEditor.jsx";
import {Calibration} from "./Views/Calibration/Calibration.jsx";
import {MesureList} from "./Views/Mesure/MesureList.jsx";
import {MesurePrepare} from "./Views/Mesure/MesurePrepare.jsx";
import {MesureData} from "./Views/Mesure/MesureData.jsx";
import ErrorBoundary from "./components/Utils/ErrorBoundary.jsx";


/* Custom socket events */
const blHasTimeout = new CustomEvent('blTimeout', { detail: { message: 'Bluetooth connection timeout' } });
const blIsConnected = new CustomEvent('blConnected', { detail: { message: 'Bluetooth connection established' } });


function App() {
    const [user, setUser] = useState(null)
    const [blConnected, setBlConnected] = useState(false)
    const [checkTime, setCheckTime] = useState(1000)

    useEffect(() => {
        myEel.set_host("ws://localhost:8888");

        const interval = setInterval(handleBl, checkTime);

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
                setCheckTime(15000)
            }else if(!blConnected && r.connected){
                setBlConnected(true);
                setCheckTime(5000)
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
                            <Route path={"patient/:id"} element={<PatientEditor/>}/>
                            <Route path={"calibration"} element={<Calibration/>}/>
                            <Route path={"patient/:id/mesures"} element={<MesureList/>}/>
                            <Route path={"patient/:id/mesure/:idmesure"} element={<MesurePrepare/>}/>
                            <Route path={"mesure/:id"} element={<MesureData/>}/>

                            <Route path={"*"} element={<NoMatchRoute/>}/>

                        </Route>

                </Routes>

            </UserContext.Provider>
    )
}

export default App;
