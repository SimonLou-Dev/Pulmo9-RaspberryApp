import React from 'react';
import {Link, useParams} from "react-router-dom";
import {Searcher} from "../../components/Table/Searcher.jsx";
import {UpdaterBtn} from "../../components/Table/UpdaterBtn.jsx";
import {PageNavigator} from "../../components/Table/PageNavigator.jsx";
import dateFormat from "dateformat";
import {myEel} from "../../MyEel.js";

export const MesureList = (props) => {
    const [page, setPage] = React.useState(1);
    const [pagination, setPagination] = React.useState({next_page: null, prev_page: null});
    const [mesures, mesuresList] = React.useState([]);

    let {id} = useParams("id")

    React.useEffect(() => {
        searcher();
    }, []);

    const searcher = async (_page) => {

        if(_page == page ) return;
        if (_page === undefined) _page = page;
        setPage(_page);


        await myEel.list_mesure(id, _page )().then((result) => {
            mesuresList(result.mesures)
            console.log(result)
            setPagination({

                next_page: (result.pages === _page) ? null : _page + 1,
                prev_page: (_page === 1) ? null : _page - 1,
            })
            if(result.mesures.length === 0) setPagination({next_page: null, prev_page: null});
        });

    }

    return (
        <div className={"MesureList"}>
            <section className={'table'}>
                <div className={'table-header'}>
                    <Link to={'/patient/' + id +'/mesure/0'} className={"btn --big"}>Ajouter</Link>
                    <UpdaterBtn callback={searcher}/>
                    <PageNavigator prev={()=> {searcher(page-1)}} next={()=> {searcher(page+1)}} prevDisabled={(pagination.prev_page === null)} nextDisabled={(pagination.next_page === null)}/>
                </div>
                <div className={'table-content'}>
                    <table>
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>fréquence</th>
                            <th>date</th>
                            <th>médecin</th>
                            <th>résultat</th>
                            <th/>
                        </tr>
                        </thead>
                        <tbody>
                        {mesures && mesures.map((mesure)=>
                            <tr key={mesure[0]} >
                                <td>{mesure[0]}</td>
                                <td>{mesure[2] + " " + mesure[1]}</td>
                                <td>{dateFormat(mesure[3], 'dd/mm/yyyy')}</td>
                                <td >{mesure[4]  === "0" ? "Homme":"femme"} </td>
                                <td><Link to={"/patient/" + mesure[0]}><img src={'../../assets/icons/editer.png'} alt={''}/></Link> </td>
                            </tr>
                        )}

                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    )
}