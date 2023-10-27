import React from 'react';
import {Searcher} from "../../components/Table/Searcher.jsx";
import {UpdaterBtn} from "../../components/Table/UpdaterBtn.jsx";
import {PageNavigator} from "../../components/Table/PageNavigator.jsx";
import dateFormat from "dateformat";
import {Link} from "react-router-dom";
import {myEel} from "../../MyEel.js";

export const PatientList = (props) => {
    const [search, setSearch] = React.useState('');
    const [page, setPage] = React.useState(1);
    const [pagination, setPagination] = React.useState({next_page: null, prev_page: null});
    const [patients, setPatients] = React.useState([]);

    React.useEffect(() => {
        searcher();
    }, []);

    const searcher = async (_search, _page) => {

        if(_page == page && _search.length < 3) return;

        if (_page === undefined) _page = page;
        if (_search === undefined) _search = search;

        setPage(_page);
        setSearch(_search);

        await myEel.get_patients(_search, _page)().then((result) => {
            setPatients(result.patients)
            console.log(result)


            setPagination({

                next_page: (result.pages === _page) ? null : _page + 1,
                prev_page: (_page === 1) ? null : _page - 1,
            })
            if(result.patients.length === 0) setPagination({next_page: null, prev_page: null});
        });
    }


    return (
        <div className={"PatientList"}>
            <section className={'table'}>
                <div className={'table-header'}>
                    <Link to={'/patient/0'} className={"btn --big"}>Ajouter</Link>
                    <Searcher value={search} callback={(v) => {searcher(v)}} placeholder={"nom OU prénom OU date de naissance"}/>
                    <UpdaterBtn callback={searcher}/>
                    <PageNavigator prev={()=> {searcher(search,page-1)}} next={()=> {searcher(search,page+1)}} prevDisabled={(pagination.prev_page === null)} nextDisabled={(pagination.next_page === null)}/>
                </div>
                <div className={'table-content'}>
                    <table>
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>prénom nom</th>
                            <th>date de naissance</th>
                            <th>sexe</th>
                            <th/>
                        </tr>
                        </thead>
                        <tbody>
                        {patients && patients.map((patient)=>
                            <tr key={patient[0]} >
                                <td>{patient[0]}</td>
                                <td>{patient[2] + " " + patient[1]}</td>
                                <td>{dateFormat(patient[3], 'dd/mm/yyyy')}</td>
                                <td >{patient[4]  === "0" ? "Homme":"femme"} </td>
                                <td><Link to={"/patient/" + patient[0]}><img src={'../../assets/icons/editer.png'} alt={''}/></Link> </td>
                            </tr>
                        )}

                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    )
}