import React from 'react';
import ReactDOM from 'react-dom';
import Server from './controllers/ServerControllers';
import Dice from './pages/dice';
import Splash from './pages/splash';
import Settings from './pages/settings';
import Character from './pages/character';
Server.init();

ReactDOM.render(<Splash />, document.getElementById('root'));
//ReactDOM.render(<Dice />, document.getElementById('root'));
//ReactDOM.render(<Character />, document.getElementById('root'));
//ReactDOM.render(<Settings />, document.getElementById('root'));
