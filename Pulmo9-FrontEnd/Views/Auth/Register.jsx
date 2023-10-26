import React, {useContext, useEffect} from 'react';
import {Link, useNavigate} from "react-router-dom";
import userContext from "../../components/Context/UserContext.jsx";
import {myEel} from "../../MyEel.js";

export const Register = (props) => {
    const user = useContext(userContext)
    const navigate = useNavigate()
    const [error, setError] = React.useState({})
    const [name, setName] = React.useState("")
    const [surname, setSurname] = React.useState("")

    useEffect(() => {
        if(user.user !== null) {
            navigate("/patients")
        }
    }, []);

    const register = async () => {
        let create_error = {}
        if (name.length < 2) Object.assign(create_error, {name: ["Le nom doit faire au moins 2 caractères"]})
        if (surname.length < 2) Object.assign(create_error, {surname: ["Le prénom doit faire au moins 2 caractères"]})

        setError(create_error)
        if (create_error.length > 0) return;

        await myEel.add_doctor(name, surname)().then((r) => {
            if(r){
                navigate("/login")
            }
        })
    }

    return (
        <div className={"auth"}>
            <div className={"auth-card"}>
                <div className={"auth-card-header"}>
                    <h1>Ajouter un docteur</h1>
                </div>
                <div className={"auth-card-body flex-row-evenly "}>
                    <div className={"form --all-sized flex-column "}>
                        <div className={"form-item flex-column"}>
                            <label>Nom</label>
                            <input type={"text"} placeholder={"Saisir votre nom"} className={"form-item " + (error.name ? 'form-error': '')} value={name} onChange={(v) => setName(v.target.value)}/>
                            {error.name && error.name.length > 0 &&
                                <ul className={'error-list'}>
                                    {error.name && error.name.map((item)=>
                                        <li>{item}</li>
                                    )}
                                </ul>
                            }
                        </div>
                        <div className={"form-item flex-column"}>
                            <label>Prénom</label>
                            <input type={"text"} placeholder={"Saisir votre prénom"} className={"form-item " + (error.surname ? 'form-error': '')} value={surname} onChange={(v) => setSurname(v.target.value)}/>
                            {error.surname && error.surname.length > 0 &&
                                <ul className={'error-list'}>
                                    {error.surname && error.surname.map((item)=>
                                        <li>{item}</li>
                                    )}
                                </ul>
                            }
                        </div>
                    </div>
                </div>
                <div className={"auth-card-footer flex-row-evenly"}>
                    <Link to={"/login"} className={"btn"}>retour</Link>
                    <button onClick={register} className={"btn"} >valider</button>
                </div>
            </div>
        </div>
    )
}