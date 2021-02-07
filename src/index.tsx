import React from 'react';
import ReactDOM from 'react-dom';
import Server from './controllers/ServerControllers';
import Dice from './pages/dice';
import Splash from './pages/splash';
import Settings from './pages/settings';
import Character from './pages/character';
import GlobalState from './global_state';

Server.init();

interface IProps {

}

interface IState {
	location: number;
	loaded: boolean;
}

export default class Main extends React.Component<IProps, IState> {

	constructor(props: any) {
		super(props);
		this.state = {
			location: 0,
			loaded: false
		};

		Server.get().onEvent("char_sheet").subscribe((data) => {
            GlobalState.player_character = JSON.parse(data.char_sheet);
			console.log("Received character sheet");
			console.log(GlobalState.player_character);
        });

		setTimeout(() => {this.setState({location:3, loaded:true})}, 2000);
	}

	handlePress(loc: number) {
		let newState: IState = this.state;
		newState.location = loc;
		this.setState(newState);
	}

	render() {
	let page = <Splash />
	if (this.state.location === 0) {
		page = (
			<Splash />
		);
	} else if (this.state.location === 1) {
		page = (
			<Dice />
		);
	} else if (this.state.location === 2 && GlobalState.player_character != null) {
		page = (
			<Character />
		);
	} else {
		page = (
			<Settings />
		);
	}

	let footer = <nav></nav>;
	if (this.state.loaded) {
		footer = (
			<nav className="navbar navbar-inverse navbar-fixed-bottom text-center">
				<div className="row">
				<a className="btn btn-info" role="button" onClick={()=>this.handlePress(1)}>Dice</a>
				<a className="btn btn-info" role="button" onClick={()=>this.handlePress(2)}>Character</a>
				<a className="btn btn-info" role="button" onClick={()=>this.handlePress(3)}>Settings</a>
				</div>
			</nav>
		)
	}

	return (
		<div>
			{page}
			{footer}
			<br />
		</div>
	);
	}
}

ReactDOM.render(<Main />, document.getElementById('root'));