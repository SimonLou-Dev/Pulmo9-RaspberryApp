import React, {useEffect, useState} from 'react';
import {Link, useParams} from "react-router-dom";
import {myEel} from "../../MyEel.js";

export const PatientEditor = (props) => {
    let {id} = useParams("id")

    const [nom, setNom] = useState("")
    const [prenom, setPrenom] = useState("")
    const [dateNaissance, setDateNaissance] = useState("")
    const [taille, setTaille] = useState("")
    const [poids, setPoids] = useState("")
    const [sexe, setSexe] = useState(3)

    const[ready, setReady] = useState(false)

    const [errors, setErrors] = useState([])


    useEffect(  () => {
    getPatient();

    }, []);

    const getPatient = async () => {
        if(id !== 0) {
            //Récupérer les infos du patient
            myEel.get_patient(id)().then((result) => {
                setNom(result[1])
                setPrenom(result[2])
                setDateNaissance(result[4])
                setTaille(result[5])
                setPoids(result[6])
                setSexe(result[3])
                setReady(true)
            })
        }
    }

    const update =  async () => {
        let _errors = {}

        //Faire la validation
        if(nom.length === 0){
            Object.assign(_errors, {nom: ["Le nom est obligatoire"]})
        }

        if(prenom.length === 0){
            Object.assign(_errors, {prenom: ["Le prénom est obligatoire"]})
        }

        if(dateNaissance.length === 0){
            Object.assign(_errors, {dateNaissance: ["La date de naissance est obligatoire"]})
        }

        if(taille.length === 0){
            Object.assign(_errors, {taille: ["La taille est obligatoire"]})
        }

        if(poids.length === 0){
            Object.assign(_errors, {poids: ["Le poids est obligatoire"]})
        }

        if(sexe === 3){
            Object.assign(_errors, {sexe: ["Le sexe est obligatoire"]})
        }

        if(Object.keys(_errors).length > 0) {
            setErrors(_errors)
            return;
        }

        //Enregistrer le patient
        await myEel.create_patient( nom, prenom, dateNaissance, taille, poids, sexe, id)().then((result) => {
            console.log(result)
            id = 0
            if(result && id !== 0){
                console.log("Patient enregistré")
            }else if(id === 0){
                console.log(result)
                id = result[0]
                setReady(true)
            }
        })

    }


    return (
        <div className={"PatientEditor"}>

            <div className={"card"}>
                <div className={"card-header"}>
                    <h2>{ id === 0 ? "Ajouter" : "Modifier"} un patient</h2>
                </div>
                <div className={"card-body flex-column"}>
                    <div className={"form-item flex-column"}>
                        <label>Prenom</label>
                        <input type={"text"} placeholder={"Saisir le prénom du patient"} className={"form-item " + (errors.prenom ? 'form-error': '')} value={prenom} onChange={(e) => setPrenom(e.target.value)}/>
                    </div>
                    {errors.prenom && errors.prenom.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.prenom && errors.prenom.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }
                    <div className={"form-item flex-column"}>
                        <label>Nom</label>
                        <input type={"text"} placeholder={"Saisir le nom du patient"} className={"form-item "+ (errors.nom ? 'form-error': '')} value={nom} onChange={(e) => setNom(e.target.value)}/>
                    </div>
                    {errors.nom && errors.nom.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.nom && errors.nom.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }
                    <div className={"form-item flex-column"}>
                        <label>Date de  naissance</label>
                        <input type={"date"} placeholder={"JJ-MM-AAAA"} className={"form-item " + (errors.dateNaissance ? 'form-error': '')} value={dateNaissance} onChange={(e) => setDateNaissance(e.target.value)}/>
                    </div>
                    {errors.dateNaissance && errors.dateNaissance.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.dateNaissance && errors.dateNaissance.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }
                    <div className={"form-item flex-column"}>
                        <label>Taille</label>
                        <input type={"number"} placeholder={"En cm"} className={"form-item " + (errors.taille ? 'form-error': '')} value={taille} onChange={(e) => setTaille(e.target.value)}/>
                    </div>
                    {errors.taille && errors.taille.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.taille && errors.taille.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }
                    <div className={"form-item flex-column"}>
                        <label>Poids</label>
                        <input type={"number"} placeholder={"en kg"} className={"form-item " + (errors.poids ? 'form-error': '')} value={poids} onChange={(e) => setPoids(e.target.value)}/>
                    </div>
                    {errors.poids && errors.poids.length > 0 &&
                        <ul className={'error-list'}>
                            {errors.poids && errors.poids.map((item)=>
                                <li>{item}</li>
                            )}
                        </ul>
                    }
                    <div className={"form-item flex-column"}>
                        <label>Sexe</label>
                        <select className={"form-item " + (errors.sexe ? 'form-error': '')} value={sexe} onChange={(e) => setSexe(e.target.value)}>
                            <option value={3} disabled={true}>Choississez le sexe</option>
                            <option value={0}>Homme</option>
                            <option value={1}>Femme</option>
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
                    <button className={"btn "} onClick={update}>Enregistrer</button>
                    <Link className={"btn " + (ready? "" : "disabled")} to={(ready? "/patient/" + id + "/mesures" : "")}>mesures</Link>
                </div>
            </div>

        </div>
    )
}