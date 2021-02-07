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

    Server.get().onEvent("roll_history").subscribe(() => {
      this.forceUpdate();
    });

    Server.get().onEvent("stream_link").subscribe(() => {
      this.forceUpdate();
    });

    Server.get().onEvent("new_roll_result").subscribe(() => {
      this.forceUpdate();
    });

  }

  requestDiceReading(e: any, dice: string, mod: number) {
    e.preventDefault();
    Server.get().send('init_roll', [dice, mod]);
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

    let recent_rolls: any[] = GlobalState.recent_results.slice(0).reverse().map((result: string, index) =>
      <tr key={index}>
        <td>{result[0]}</td>
        <td>{result[1]}</td>
        <td>{result[2]}</td>
      </tr>
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
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "d20", 0)}>d20</a>
            <a className="btn btn-info" onClick={(e) => this.requestDiceReading(e, "2d6", 5)}>2d6+5</a>
          </div>
        </div><br />


        <div className="container">
          <div className="row">
            <div className="col-xs-12">
              <div className="panel panel-warning">
                <div className="embed-responsive embed-responsive-16by9 waiting-fo">
                  <img className="embed-responsive-item" src={GlobalState.cam_enabled?"http://10.0.0.5/webcam/?action=stream":undefined}></img>
                  Waiting for dice...
                </div>
              </div>
              <table className="table roll-results">
                <thead>
                  <tr>
                    <td>Name</td>
                    <td>Roll</td>
                    <td>Result</td>
                  </tr>
                </thead>
                <tbody>
                  {recent_rolls}
                </tbody>
              </table>
            </div>
          </div>
        </div><br />
      </div>
    );
  }
}