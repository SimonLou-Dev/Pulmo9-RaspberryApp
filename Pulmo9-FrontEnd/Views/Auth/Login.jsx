import React, {useContext, useEffect} from 'react';
import {Link, useNavigate} from "react-router-dom";
import userContext from "../../components/Context/UserContext.jsx";
import blImage from "../../assets/bluetooth.png";
import {myEel} from "../../MyEel.js";


export const Login = (props) => {
    const user = useContext(userContext)
    const navigate = useNavigate()
    const [selectedDoctor, selectDoctor] = React.useState(0)
    const [error, setError] = React.useState({})
    const [doctors, setDoctors] = React.useState([])


    useEffect(() => {
        if(user.user !== null) {
            navigate("/patients")
        }

        getDoctors()


    }, []);

    const getDoctors = async () => {
        await myEel.get_doctors()().then((r) => {
            setDoctors(r)
        })
    }


    const login = async () => {
        let create_error = {}
        if(selectedDoctor === 0)  Object.assign(create_error, {doctor:["Veuillez choisir un médecin"]})
        await myEel.login(selectedDoctor)().then((r) => {

            if(r.logged){
                navigate("/patients")
                user.setUser({
                    id: r.doctor[0],
                    name: r.doctor[1],
                    surname: r.doctor[2],
                })
            }else{
                Object.assign(create_error, {doctor:["Le médecin n'a pas été trouvé"]})

            }
        })
        setError(create_error)
    }

        return (
            <div className={"auth"}>
                <div className={"auth-card"}>
                    <div className={"auth-card-header"}>
                        <h1>Connexion</h1>
                    </div>
                    <div className={"auth-card-body flex-row-evenly"}>
                        <div className={"form --all-sized flex-column"}>
                            <div className={"form-item flex-column"}>
                                <label>Médecin</label>
                                <select className={"form-input " + (error.doctor ? 'form-error': '')} value={selectedDoctor} onChange={(v) => selectDoctor(v.target.value)}>
                                    <option value={0} disabled={true}>Choisir un médecin</option>
                                    {doctors.map((item) =>
                                        <option value={item[0]} key={item[0]}>{item[1] + " " + item[2]}</option>
                                    )}
                                </select>
                                {error.doctor && error.doctor.length > 0 &&
                                    <ul className={'error-list'}>
                                        {error.doctor && error.doctor.map((item)=>
                                            <li>{item}</li>
                                        )}
                                    </ul>
                                }


                            </div>
                        </div>
                    </div>
                    <div className={"auth-card-footer flex-row-evenly"}>
                        <Link to={"/"} className={"btn"}>retour</Link>
                        <button onClick={login} className={"btn"}>connexion</button>
                        <Link to={"/register"} className={"btn"}>s&apos;inscrire</Link>
                    </div>
                </div>
            </div>
        )
}
