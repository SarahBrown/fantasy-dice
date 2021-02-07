import React from 'react';
import ReactDOM from 'react-dom';
import Server from './controllers/ServerControllers';
import Dice from './pages/dice';
import Splash from './pages/splash';
import Settings from './pages/settings';
import Character from './pages/character';
import GlobalState from './global_state';
import Retro from './pages/retro';

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

		Server.get().onEvent("player_list").subscribe((data) => {
			GlobalState.player_list = JSON.parse(data.player_list);
			console.log("Received player_list");
			console.log(GlobalState.player_list);
		});

		Server.get().onEvent("roll_history").subscribe((data) => {
			let temp:any = JSON.parse(data.roll_history);
			console.log("Received roll_history");
			console.log(temp);
			GlobalState.recent_results = temp;
		});

		Server.get().onEvent("new_roll_result").subscribe(() => {
			console.log("Received new_roll_result");
			GlobalState.cam_enabled = false;
		});
	
		Server.get().onEvent("stream_link").subscribe(() => {
			console.log("Received stream_link");
			GlobalState.cam_enabled = true;
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
	} else if (this.state.location === 1 && GlobalState.player_list != null) {
		page = (
			<Dice />
		);
	} else if (this.state.location === 2 && GlobalState.player_character != null) {
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
				<a className="btn btn-info" role="button" onClick={()=>this.handlePress(4)}>Retro</a>
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