import React, {useContext, useEffect} from 'react';
import UserContext from "../components/Context/UserContext.jsx";
import {Link, Outlet, useNavigate} from "react-router-dom";
import ErrorBoundary from "../components/Utils/ErrorBoundary.jsx";


export const Layout = (props) => {
    const user = useContext(UserContext)
    const navigate = useNavigate()

    useEffect(() => {


        if(user.user === null) {
            navigate("/login")
        }
    }, []);

    const logout = async () => {
        user.setUser(null)
        navigate("/login")
    }


    return (
        <div className={"Layout"}>
            <div className={"Header"}>
                <div className={"doctor_name flex-row-evenly"}>
                    <button className={"button rounded"} onClick={logout}>
                        <img src={"../assets/icons/logout.png"}/>
                    </button>
                    <h3>{user.user.name + " " + user.user.surname}</h3>
                </div>
                <div className={"menu"}>
                    <ul>
                        <li><Link to={"/patients"}>dossier patient</Link></li>
                        <li><Link to={"/calibration"}>Calibration</Link></li>
                    </ul>
                </div>

            </div>

            <div className={"Content"}>
                <ErrorBoundary>
                    <Outlet/>
                </ErrorBoundary>
            </div>



        </div>
    )
}

/*

Put des route genre ReactView
<Route path={'/patients/rapport'} component={Rapport}/>
 */