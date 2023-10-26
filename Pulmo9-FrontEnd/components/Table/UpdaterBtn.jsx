import React from 'react';

export const UpdaterBtn = (props) => {


    return (
        <button className={'btn updater'} onClick={()=>props.callback()}>
            <img alt={""} src={"../../assets/icons/update.png"}/>
        </button>
    )
}