import React from 'react';

export const PageNavigator = (props) => {


    return (
        <div className={'PageNavigator'}>
            <button onClick={props.prev} disabled={(props.prevDisabled)}>
                <img src={'../../assets/icons/left-arrow.png'} alt={''} className={'navigator-btn'}/>
            </button>
            <button onClick={props.next} disabled={(props.nextDisabled)}>
                <img src={'../../assets/icons/right-arrow.png'} alt={''} className={'navigator-btn'}/>
            </button>
        </div>
    )
}