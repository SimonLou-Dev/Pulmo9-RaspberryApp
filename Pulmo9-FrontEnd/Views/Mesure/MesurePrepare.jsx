import React, {useEffect} from 'react';
import {Link, useParams} from "react-router-dom";

export const MesurePrepare = (props) => {
    const [errors, setErrors] = React.useState([])
    const [frequency, setFrequency] = React.useState(0)
    const [ready, setReady] = React.useState(false)

    let {id} = useParams("id")
    let {mesureId} = useParams("idmesure")

    useEffect(() => {
        if(mesureId != 0 ){
            //ça redirige vers la mesure
        }

    }, []);

    const save = async () => {

    }


    return (
        <div className={"PatientEditor"}>

            <div className={"card"}>
                <div className={"card-header"}>
                    <h2> ajouter une mesure</h2>
                    <h3></h3>
                </div>
                <div className={"card-body flex-column"}>

                    <div className={"form-item flex-column"}>
                        <label>Fréquence</label>
                        <select className={"form-item " + (errors.sexe ? 'form-error': '')} value={frequency} onChange={(e) => setFrequency(e.target.value)}>
                            <option value={0} disabled={true}>Choississez la fréquence</option>
                            <option value={4}>4 Hz</option>
                            <option value={8}>8 Hz</option>
                            <option value={12}>12 Hz</option>
                            <option value={20}>20 Hz</option>
                            <option value={30}>30 Hz</option>

                        </select>
                    </div>
                    {errors.sexe && errors.sexe.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.sexe && errors.sexe.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }

                </div>
                <div className={"card-footer flex-row-evenly"}>
                    <Link className={"btn "} to={"/patients"}>Retour</Link>
                    <button className={"btn "} onClick={save}>Enregistrer</button>
                    <Link className={"btn " + (ready? "" : "disabled")} to={(ready? "mesure/:id" : "")}>continuer</Link>
                </div>
            </div>

        </div>
    )
}