import React from 'react';
export const Searcher = (props) => {



    return (
        <div className={'searcher'}>
            <img src={"../../assets/icons/search.png"} alt={''} className={'searcher-icon'}/>
            <input type={'text'} className={'searcher-input'} placeholder={props.placeholder} value={props.value} onChange={(e)=>{props.callback(e.target.value)}}/>
        </div>
    )
}