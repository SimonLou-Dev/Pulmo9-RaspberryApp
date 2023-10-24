import {useContext} from 'react';
import {Link} from "react-router-dom";
import userContext from "../../components/Context/UserContext.jsx";


export const Login = (props) => {
    const user = useContext(userContext)

    const login = () => {
        user.setUser({name: "test"})
    }


    const test =  async () => {

    }


        return (
            <>
                    <h1>Connecte toi</h1>
                    <button onClick={login}>Login</button>
                    <button onClick={test}>test</button>
                    <Link to={"/patients"}>Retour</Link>
            </>
        )
}
