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

  }

  render() {

    let players: any[] = GlobalState.player_list.map((plr:string[]) =>
    <div className="col-xs-4" key={plr[0]}>
      <div className="panel">
        <div className="panel-body"><img src={plr[2]} className="img-responsive" style={{ width: "100%" }}
          alt="Image" />{plr[1]}</div>
      </div>
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
            <div className="col-xs-12">
              <div className="panel panel-warning">
                <div className="embed-responsive embed-responsive-16by9">
                  <iframe className="embed-responsive-item" src=""></iframe>
                </div>
              </div>
            </div>

          </div>
        </div><br />
      </div>
    );
  }
}