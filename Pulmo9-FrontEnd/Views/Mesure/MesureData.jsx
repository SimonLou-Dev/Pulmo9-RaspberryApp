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
    const [mesureTime, setMesureTime] = React.useState(0)



    useEffect(() => {

        getMesureInfos(); //Call bloquant pour pouvoir tout mettre dans les options

        //initGraph()




        const interval = setInterval(async () => {
            setRunner((prevState) => prevState + 1)

        }, updateRate);
        return () => clearInterval(interval);


    }, []);

    const initGraph = (frequency = data[1]) => {

        const secDuration = frequency * 8
        const softMax = secDuration * 30


        setOptions( {
            chart: {
                type: 'spline',
                animation: false,
            },
            title: {
                text: 'Mesure'
            },
            xAxis: {
                tickInterval: secDuration,
                softMax: softMax,
                labels: {
                    formatter: function () {
                        return this.value / secDuration;
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

    }

    const getMesureInfos =  async () => {
        await myEel.get_mesure(id)().then((r) => {
            setData(r)
            setUpdateRate(Math.round(1000 / r[1]))
            getSeries()
            console.log(r)
            initGraph(parseInt(r[1]))
            setMesureTime(Math.round(current * 10 / (8 * parseInt(r[1]))) / 10 + "s")
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

    const initMesure = async () => {
        await myEel.init_mesure(parseInt(data[1]), parseInt(id) )().then((r) => {
            setRunning(true)
            console.log(r)

        }).catch((e) => {
            console.log(e)
        });
    }

    const startMesure = async () => {
        console.log("start")
        await myEel.start_mesure(id)().then((r) => {
            console.log(r)
        }).catch((e) => {
            console.log(e)
        })



    }

    const stopMesure = () => {
        console.log("stop")
        myEel.stop_mesure()().then((r) => {

            console.log(r)
        }).catch((e) => {
            console.log(e)
        })

        setRunning(false)

    }




    const updateSeries = (pression, debit) => {
        const chartRef = chartComponent.current?.chart;

        pression = Object.values(pression)
        debit = Object.values(debit)


        chartRef.series[0].setData(debit)
        chartRef.series[1].setData(pression)

        setCurrent(pression.length)
        setMesureTime(Math.round(current * 10 / (8 * parseInt(data[1]))) / 10 + "s")

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
                    <p>Temps de la mesure : {mesureTime} </p>
                    {running &&
                        <>
                            <button onClick={startMesure} className={"btn"}>start</button>
                            <button onClick={stopMesure} className={"btn"}>stop</button>
                        </>
                    }

                    {!running &&
                            <button onClick={initMesure} className={"btn"}>lancer</button>
                    }

                </div>

            </div>


        </div>
    )
}