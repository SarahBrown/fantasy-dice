import React from 'react';

interface IProps {

}

interface IState {

}

export default class Splash extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }
//comment
    render() {
        return (
            <div>
                <div className="container">
                    <br/>
                    <img src="assets\loadingDragonBorder.GIF" className="img-responsive" style={{ width: "100%" }}
                        alt="Image" />
                    <h1>Welcome! <br/> Your adventure is loading!</h1>
                </div>
            </div>
        );
    }
}