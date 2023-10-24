import React, {useContext} from 'react';
import blImage from '../assets/bluetooth.png'
import userContext from "../components/Context/UserContext.jsx";
import {myEel} from "../MyEel.js";


export const WaitAuth = (props) => {
    const context = useContext(userContext)

    const quit = () => {
        console.log("Fired")

        myEel.get_doctors()();
    }


    return (
        <div className={"auth"}>
            <div className={"auth-card"}>
                <div className={"auth-card-header"}>
                    <h1>Pulmo9</h1>
                    <h6>Mesure d&apos;impédance Thoraco-Pulmonaire</h6>
                </div>
                <div className={"auth-card-body flex-row-evenly"} id={"WaitAuth"}>
                    <img src={blImage} alt={"bl"} />
                    {context.blConnected ?
                        <h2 className={"green-glow"}>Connecté</h2>
                        :
                        <h3>En attente de connexion</h3>
                    }
                </div>
                <div className={"auth-card-footer flex-row-evenly"}>
                    <button  onClick={quit} className={"btn"}>quitter</button>
                    <button  className={"btn"}>connexion</button>
                </div>
            </div>
        </div>
    )
}