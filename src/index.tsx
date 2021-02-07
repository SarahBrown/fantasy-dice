import React from 'react';
import ReactDOM from 'react-dom';
import Server from './controllers/ServerControllers';
import Dice from './pages/dice';
import Splash from './pages/splash';
import Settings from './pages/settings';
import Character from './pages/character';
import Retro from './pages/retro';

Server.init();

interface IProps {

}

interface IState {
    location: number;
}

export default class Main extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {
            location: 0
        };
    }

  handlePress(loc: number) {
    let newState: IState = this.state;
    newState.location = loc;
    this.setState(newState);
  }

  render() {
    let page = <Splash />
    if (this.state.location === 1) {
        page = (
            <Dice />
        );
    } else if (this.state.location === 2) {
        page = (
            <Character />
        );
    } else if (this.state.location === 3) {
        page = (
            <Settings />
        );
    } else if (this.state.location === 4) {
        page = (
            <Retro />
        );
    }
    
    return (
        <div>
            {page}
            <nav className="navbar navbar-inverse navbar-fixed-bottom text-center">
                <div className="row">
                <a className="btn btn-info" role="button" onClick={()=>this.handlePress(1)}>Dice</a>
                <a className="btn btn-info" role="button" onClick={()=>this.handlePress(2)}>Character</a>
                <a className="btn btn-info" role="button" onClick={()=>this.handlePress(3)}>Settings</a>
                <a className="btn btn-info" role="button" onClick={()=>this.handlePress(4)}>Retro</a>
                </div>
            </nav> 
            <br />
        </div>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById('root'));