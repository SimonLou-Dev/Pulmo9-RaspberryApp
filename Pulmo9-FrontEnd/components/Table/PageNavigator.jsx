import React from 'react';
import rightArrow from '../../assets/icons/right-arrow.png'
import leftArrow from '../../assets/icons/left-arrow.png'

export const PageNavigator = (props) => {


    return (
        <div className={'PageNavigator'}>
            <button onClick={props.prev} disabled={(props.prevDisabled)}>
                <img src={leftArrow} alt={''} className={'navigator-btn'}/>
            </button>
            <button onClick={props.next} disabled={(props.nextDisabled)}>
                <img src={rightArrow} alt={''} className={'navigator-btn'}/>
            </button>
        </div>
    )
}