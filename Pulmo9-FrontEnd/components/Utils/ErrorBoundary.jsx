import React from 'react';
import {Link} from "react-router-dom";

export default class ErrorBoundary extends React.Component {

    state = {
        hasError: false,
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.log(error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <>
                    <h1>Something went wrong.</h1>
                    <Link to={"/"}>Go Back to Home</Link>
                </>
            );
        }

        return this.props.children;
    }

}