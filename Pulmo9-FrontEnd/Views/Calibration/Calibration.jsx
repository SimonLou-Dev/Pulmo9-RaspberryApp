import React, {useState} from 'react';
import {myEel} from "../../MyEel.js";

export const Calibration = (props) => {
    const [step, setStep] = useState(0)



    return (
        <div className={"Calibration"}>

            <div className={"card"}>


                <div className={"avancement"}>
                    <div className={"avancement-status"}>
                        <div className={"avancement-status-point " + (step == 0 ? "active" : "") + (step > 0 ? "passed" : "")}/>
                        <div className={"avancement-status-point " + (step == 1 ? "active" : "") + (step > 1 ? "passed" : "")}/>
                        <div className={"avancement-status-point " + (step == 2 ? "active" : "") + (step > 2 ? "passed" : "")}/>
                        <div className={"avancement-status-point " + (step == 3 ? "active" : "") + (step > 3 ? "passed" : "")}/>
                    </div>
                </div>





                {step === 0 && <PressureCalibration nextStape={(v) => setStep(v)}/>}
                {step === 1 && <PressureAtmosphericCalibration nextStape={(v) => setStep(v)}/>}
                {step === 2 && <FlowCalibration/> }




            </div>


        </div>
    )
}


const PressureCalibration = (props) => {
    const [calibrationMode, setCalibrationMode] = useState(0)
    const [calibrationValue, setCalibrationValue] = useState(0)
    const [errors, setErrors] = useState([])
    const [internalSteps, setInternalSteps] = useState(0)
    const [calibrationRunning , setCalibrationRunning] = useState(false)

    const validateInformation = () => {
        let _errors = []
        if(calibrationMode == 0) {
            Object.assign(_errors, {"mode": ["Vous devez choisir un mode de calibration"]})
        }
        if(calibrationValue == 0) {
            Object.assign(_errors, {"value": ["Vous devez choisir une valeur de calibration"]})
        }

        if(_errors.length == 0){
            setInternalSteps(1)
        }else{
            setErrors(_errors)
        }
    }

    const inputInformation = () => {
        return (
            <div className={"card-infos-content-mode"}>
                <h3>Information de calibration</h3>
                <div className={"form-item flex-column"}>
                    <label>Mode de calibration</label>
                    <select value={calibrationMode} onChange={(e) => setCalibrationMode(e.target.value)}>
                        <option value={0} disabled={true}>choisir un mode</option>
                        <option value={1}>Avec de l'eau</option>
                        <option value={2}>Avec un manomètre</option>
                    </select>
                </div>
                {calibrationMode != 0 &&
                    <div className={"form-item flex-column"}>
                        {calibrationMode == 1 && <label>Choisir le nombre de cm d'eau</label>}
                        {calibrationMode == 2 && <label>Choisir la pression injecté (bar)</label>}
                        <input type={"text"} value={calibrationValue} placeholder={(calibrationMode == 1 ? "Valeur en cmH2O" : "Valeur en bar")} onChange={(e) => setCalibrationValue(e.target.value)}/>
                    </div>
                }
                <button className={"btn"} onClick={validateInformation} disabled={calibrationMode == 0}>Valider</button>

            </div>
        )
    }

    const retour = () => {
        setInternalSteps(0)
    }

    const sendCalibration = () => {
        let hpaPress = 0;
        if (calibrationMode == 1){
            hpaPress = calibrationValue * 0.980665
        }
        if (calibrationMode == 2){
            hpaPress = calibrationValue * 100000
        }
        setCalibrationRunning(true)
        myEel.calibrate_pression(hpaPress)().then((r) => {
            if (r){
                setInternalSteps(2)
                setTimeout(() => {
                    setCalibrationRunning(false)
                }, 3000)
            }
        })
    }

    const calibration = () => {

        return(
            <div className={"card-infos-content-calibration"}>
                <h3>Calibration</h3>
                {calibrationMode == 1 &&
                    <p>Ouvrez la machine, prennez le tuyaux avec le repère vert et mettez le dans {calibrationValue} cm d'eau. Puis cliquez sur pret</p>
                }
                {calibrationMode == 2 &&
                    <p>Injectez {calibrationValue} bar(s) dans l'entrée de la machine et cliquez sur pret</p>
                }
                <div className={"btn-group"}>
                    <button className={"btn --big"} onClick={retour}>Retour</button>
                    <button className={"btn --big"} id={"calibratePress"} onClick={sendCalibration}>Pret</button>
                </div>
            </div>
        )
    }

    const final = () => {

        return(
            <div className={"card-infos-content-calibration"}>
                <h3>Calibration</h3>
                {calibrationRunning && <p>Calibration en cours ...</p>}
                {!calibrationRunning && <p>Calibration terminé</p>}
                <div className={"btn-group"}>
                    <button className={"btn --big"} onClick={() => {setInternalSteps(1)}} disabled={calibrationRunning}>Recommencer</button>
                    <button className={"btn --big"} id={"calibratePress"} onClick={()=> props.nextStape(1)} disabled={calibrationRunning}>Suivant</button>
                </div>
            </div>
        )
    }

    return(
        <div className={"card-infos"}>
            <div className={"card-infos-title"}>
                <h2>Calibration de la pression</h2>
            </div>

            {internalSteps == 0 && inputInformation()}
            {internalSteps == 1 && calibration()}
            {internalSteps == 2 && final()}
        </div>
    )

}

const PressureAtmosphericCalibration = (props) => {
    const [internalSteps, setInternalSteps] = useState(0)
    const [calibrationRunning , setCalibrationRunning] = useState(false)

    const sendCalibration = () => {
        setCalibrationRunning(true)
        myEel.calibrate_pression_atm()().then((r) => {
            if (r){
                setInternalSteps(1)
                setTimeout(() => {
                    setCalibrationRunning(false)
                }, 3000)
            }
        })
    }

    const prepareCalibration = () => {

        return(
            <div className={"card-infos-content-calibration"}>
                <h3>Préparation</h3>
                <p>Remettez la machine en état originel. (Prennez garde a bien secher le tuyau) Puis appuyez sur pret</p>

                <div className={"btn-group"}>
                    <button className={"btn --big"} id={"calibratePress"} onClick={sendCalibration}>Pret</button>
                </div>
            </div>
        )
    }

    const final = () => {
        return(
            <div className={"card-infos-content-calibration"}>
                <h3>Calibration</h3>
                {calibrationRunning && <p>Calibration en cours ...</p>}
                {!calibrationRunning && <p>Calibration terminé</p>}
                <div className={"btn-group"}>
                    <button className={"btn --big"} onClick={() => {setInternalSteps(0)}} disabled={calibrationRunning}>Recommencer</button>
                    <button className={"btn --big"} id={"calibratePress"} onClick={()=> props.nextStape(2)} disabled={calibrationRunning}>Suivant</button>
                </div>
            </div>
        )
    }

    return (
        <div className={"card-infos"}>
            <div className={"card-infos-title"}>
                <h2>Calibration de la pression atmosphérique</h2>
            </div>

            {internalSteps == 0 && prepareCalibration()}
            {internalSteps == 1 && final()}
        </div>
    )

}


const FlowCalibration = (props) => {
    const [internalSteps, setInternalSteps] = useState(0)
    const [calibrationRunning , setCalibrationRunning] = useState(false)

    const sendCalibration = () => {
        setCalibrationRunning(true)
        myEel.calibrate_debit()().then((r) => {
            if (r){
                setInternalSteps(1)
                setTimeout(() => {
                    setCalibrationRunning(false)
                }, 3000)
            }
        })
    }

    return (
        <div className={"card-infos"}>
            <div className={"card-infos-title"}>
                <h2>Calibration du débit</h2>
            </div>

            <button className={"btn"} onClick={sendCalibration}>fullTest</button>
        </div>
    )

}


