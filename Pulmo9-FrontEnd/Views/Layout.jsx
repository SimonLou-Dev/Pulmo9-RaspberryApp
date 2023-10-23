import React, {useContext, useEffect} from 'react';
import UserContext from "../components/Context/UserContext.jsx";
import {Link, Outlet, useNavigate} from "react-router-dom";
import viteLogo from "../assets/vite.svg";

export const Layout = (props) => {
    const user = useContext(UserContext)
    const navigate = useNavigate()

    useEffect(() => {
        if(user.user === null) {
            navigate("/login")
        }
    }, []);


    return (
        <div className={"Layout"}>
            <Link to={"/login"}>Connexion</Link>
            <img src={viteLogo} alt={"vite"}/>
            <Outlet/>
        </div>
    )
}

/*

Put des route genre ReactView
<Route path={'/patients/rapport'} component={Rapport}/>
 */