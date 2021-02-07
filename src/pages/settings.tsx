import React from 'react';
import Server from '../controllers/ServerControllers';

interface IProps {

}

interface IState {
    name: string;
    room: string;
    dndb_url: string;
}

export default class Settings extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {name: "", room: "", dndb_url: ""};

        this.handleClick = this.handleClick.bind(this);
        this.handleNameChange = this.handleNameChange.bind(this);
        this.handleRoomChange = this.handleRoomChange.bind(this);
        this.handleDNDBeyondChange = this.handleDNDBeyondChange.bind(this);
    }

    handleNameChange(e: any) {
        let prevState = {...this.state};
        prevState.name = e.target.value;
        this.setState(prevState);
    }

    handleRoomChange(e: any) {
        let prevState = {...this.state};
        prevState.room = e.target.value;
        this.setState(prevState);
    }

    handleDNDBeyondChange(e: any) {
        let prevState = {...this.state};
        prevState.dndb_url = e.target.value;
        this.setState(prevState);
    }

    handleClick(e: any) {
        e.preventDefault();
        Server.get().send('join_campaign', [this.state.name, this.state.room, this.state.dndb_url]);
    }

    render() {
        return (
            <div>
                <div className="container">
                <div className = "rowForm">
                    Player Name:
                        <form onSubmit={(e)=>e.preventDefault()}>
                        <div className="col-xs-12">
                            <label>
                                <input type="text" name="name" onChange={this.handleNameChange} value={this.state.name}/>
                            </label>
                        </div>
                        </form>
                    </div>
                </div>

                <div className="container">
                <div className = "rowForm">
                        Campaign Name:
                        <form onSubmit={(e)=>e.preventDefault()}>
                        <div className="col-xs-12">
                            <label>
                                <input type="text" name="roomNum" onChange={this.handleRoomChange} value={this.state.room}/>
                            </label>
                        </div>
                        </form>
                    </div>
                </div>

                <div className="container">
                    <div className = "rowForm">
                        DND Beyond URL:
                        <form onSubmit={(e)=>e.preventDefault()}>
                        <div className="col-xs-12">
                            <label>
                                <input type="text" name="dndbeyond" onChange={this.handleDNDBeyondChange} value={this.state.dndb_url}/>
                            </label>
                        </div>

                        </form>
                    </div>
                </div>

                <div className="col-xs-12 p-10">
                        <input className="btn" type="submit" value="Submit" onClick={this.handleClick}/>
                </div>

                <div className="container">
                    <img src="assets\loadingDragonBorder.GIF" className="img-responsive" style={{ width: "100%" }}
                        alt="Image" />
                </div>
            </div>
        );
    }
}