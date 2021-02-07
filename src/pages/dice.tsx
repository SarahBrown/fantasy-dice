import React from 'react';
import Server from '../controllers/ServerControllers';
import GlobalState from '../global_state';

interface IProps {

}

interface IState {

}

export default class Dice extends React.Component<IProps, IState> {

  constructor(props: any) {
    super(props);
    this.state = {};

    Server.get().onEvent("player_list").subscribe(() => {
      this.forceUpdate();
    });

    Server.get().onEvent("new_roll_result").subscribe(() => {
      this.forceUpdate();
    });

  }

  requestDiceReading(e: any, dice: string) {
    e.preventDefault();
    Server.get().send('init_roll', [dice, 0]);
  }

  render() {

    let players: any[] = GlobalState.player_list.map((plr: string[]) =>
      <div className="col-xs-4" key={plr[0]}>
        <div className="panel">
          <div className="panel-body"><img src={plr[2]} className="img-responsive" style={{ width: "100%" }}
            alt="Image" />{plr[1]}</div>
        </div>
      </div>
    );

    let recent_rolls: any[] = GlobalState.recent_results.map((result: string, index) =>
      <div className="col-xs-4" key={index}>
        {result}
      </div>
    );

    return (
      <div>
        <div className="container">
          <div className="row">
            {players}
          </div>
        </div><br />

        <div className="container">
          <div className="row">
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d6")}>d6</a>
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d8")}>d8</a>
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d10")}>d10</a>
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d12")}>d12</a>
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d20")}>d20</a>
          </div>
        </div><br />


        <div className="container">
          <div className="row">
            <div className="col-xs-12">
              <div className="panel panel-warning">
                <div className="embed-responsive embed-responsive-16by9">
                  <img className="embed-responsive-item" src="//:0"></img>
                </div>
              </div>
              {recent_rolls}
            </div>
          </div>
        </div><br />
      </div>
    );
  }
}