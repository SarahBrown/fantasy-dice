import React from 'react';

interface IProps {

}

interface IState {

}

export default class Settings extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div>
                <div className="container">
                <div className = "rowForm">
                Room Number:
                        <form>
                        <div className="col-xs-8">
                            <label>
                                <input type="text" name="roomNum" />
                            </label>
                        </div>

                        <div className="col-xs-3">
                            <input type="submit" value="Submit" />
                        </div>

                        </form>
                    </div>
                </div><br />

                <div className="container">

                    <div className = "rowForm">
                    DND Beyond URL:
                        <form>
                        <div className="col-xs-8">
                            <label>
                                <input type="text" name="dndbeyond" />
                            </label>
                        </div>

                        <div className="col-xs-3">
                            <input type="submit" value="Submit" />
                        </div>

                        </form>
                    </div>
                </div><br />

                <div className="container">
                    <img src="assets\loadingDragonBorder.GIF" className="img-responsive" style={{ width: "100%" }}
                        alt="Image" />
                </div>
            </div>
        );
    }
}