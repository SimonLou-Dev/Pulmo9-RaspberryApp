import React, {useEffect, useRef} from 'react';
import Highcharts , {Chart} from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import {Link, useParams} from "react-router-dom";
import {myEel} from "../../MyEel.js";


export const MesureData = (props) => {
    let {id} = useParams("id")

    const chartComponent = useRef()

    const [Options, setOptions] = React.useState({})
    const [current, setCurrent] = React.useState(0)
    const [running, setRunning] = React.useState(false)
    const [runner , setRunner] = React.useState(null)

    const [data, setData] = React.useState([])
    const [updateRate, setUpdateRate] = React.useState(250)



    useEffect(() => {

        getMesureInfos(); //Call static pour pouvoir tout mettre dans les options

        setOptions( {
            chart: {
                type: 'spline',
                animation: false,
            },
            title: {
                text: 'Mesure'
            },
            xAxis: {
                tickInterval: 8*updateRate,
                softMax: 30*8*updateRate,
                labels: {
                    formatter: function () {
                        return this.value / (8*updateRate);
                    }
                }
            },
            yAxis: [
                {
                    title: {
                        text: 'Debit (L/s)',
                    },
                },
                {
                    title: {
                        text: 'Pression (hPa)',
                    },
                    opposite: true
                }
            ],
            series: [
                {
                    name: "debit",
                    type: 'area',
                    yAxis: 0,
                    data: [],
                },{
                    name: "pression",
                    type: 'line',
                    yAxis: 1,
                    data: [],
                }

            ],

        })



        const interval = setInterval(async () => {
            setRunner((prevState) => prevState + 1)

        }, getMesureInfos);
        return () => clearInterval(interval);


    }, []);

    const getMesureInfos =  () => {
        myEel.get_mesure(id)().then((r) => {
            setData(r)
            setUpdateRate(250)
        });
    }


    useEffect(() => {
        if (!running) return;
        getSeries()
    }, [runner]);

    const getSeries = async () => {
         await myEel.get_mesure_points(id)().then((r) => {
            updateSeries(r.pression, r.debit)

        });

    }

    const updateSeries = (pression, debit) => {
        const chartRef = chartComponent.current?.chart;


        for (let i = current; i < pression.length; i++) {
            chartRef.series[0].addPoint(debit[i])
            chartRef.series[1].addPoint(pression[i])

        }

        setCurrent((prevState) => prevState + 8)

    }




    return (
        <div className={"MesureData"}>

            <div className={"mesure-container"}>
                <div className={"mesure-container-title"}>
                </div>
                <div className={"mesure-container-charts"}>
                    <HighchartsReact  options={Options} highcharts={Highcharts} ref={chartComponent} />

                </div>
                <div className={"mesure-container-footer"}>
                    <p>Nombre de mesures affiches {current}</p>
                    <button className={"btn --big"} onClick={getSeries}>Ajouter</button>
                    <button className={"btn --big"} onClick={() => {setRunning(true)}}>Start</button>
                    <button className={"btn --big"} onClick={() => {setRunning(false)}}>Stop</button>
                </div>

            </div>


        </div>
    )
}