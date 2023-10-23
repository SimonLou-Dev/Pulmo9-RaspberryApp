import React from 'react'
import ReactDOM, {createRoot} from 'react-dom/client'
import App from './App.jsx'
import './scss/app.scss'
import {BrowserRouter} from "react-router-dom";





if (document.getElementById('root')) {
    const domNode = document.getElementById('root');
    const root = createRoot(domNode);
    root.render(<React.StrictMode>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </React.StrictMode>)

}



