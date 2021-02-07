import React from 'react';
import ReactDOM from 'react-dom';
import Server from './controllers/ServerControllers';
import Dice from './pages/dice';

Server.init();

ReactDOM.render(<Dice />, document.getElementById('root'));