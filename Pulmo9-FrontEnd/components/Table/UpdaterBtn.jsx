import React from 'react';
import update from '../../assets/icons/update.png'
export const UpdaterBtn = (props) => {


    return (
        <button className={'btn updater'} onClick={()=>props.callback()}>
            <img alt={""} src={update}/>
        </button>
    )
}