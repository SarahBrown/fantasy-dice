import React from 'react';

interface IProps {

}

interface IState {

}

export default class Dice extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div>
            <div className="container">
                <div className="row">
                    <div className="col-xs-4">
                        <div className="panel">
                        <div className="panel-body"><img src="assets\profilePic1.PNG" className="img-responsive" style={{width: "100%"}}
                            alt="Image" /></div>
                        </div>
                    </div>
                    <div className="col-xs-4">
                        <div className="panel">
                        <div className="panel-body"><img src="assets\profilePic1.PNG" className="img-responsive" style={{width: "100%"}}
                            alt="Image" /></div>
                        </div>
                    </div>
                    <div className="col-xs-4">
                        <div className="panel">
                        <div className="panel-body"><img src="assets\profilePic1.PNG" className="img-responsive" style={{width: "100%"}}
                            alt="Image" /></div>
                        </div>
                    </div>
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