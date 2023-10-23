import React, {useEffect} from 'react';
import {useNavigate} from "react-router-dom";

export const NoMatchRoute = (props) => {
    const navigate = useNavigate()


    useEffect(() => {
        navigate("/patients")
    }, []);

    return (
        <div className={"NoMatchRoute"}>

        </div>
    )
}