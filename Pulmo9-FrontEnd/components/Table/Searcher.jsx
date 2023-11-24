import React from 'react';
import search from '../../assets/icons/search.png'
export const Searcher = (props) => {



    return (
        <div className={'searcher'}>
            <img src={search} alt={''} className={'searcher-icon'}/>
            <input type={'text'} className={'searcher-input'} placeholder={props.placeholder} value={props.value} onChange={(e)=>{props.callback(e.target.value)}}/>
        </div>
    )
}