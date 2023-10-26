import React, {useContext, useEffect} from 'react';
import UserContext from "../components/Context/UserContext.jsx";
import {Link, Outlet, useNavigate} from "react-router-dom";


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
            <Outlet/>
        </div>
    )
}

/*

Put des route genre ReactView
<Route path={'/patients/rapport'} component={Rapport}/>
 */