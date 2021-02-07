import React from 'react';

interface IProps {

}

interface IState {

}

export default class Retro extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }

//comment
    render() {
        return (
            <div>
                <div className="container">
                    <br/>
                    <div className="retro">
                        <img src="assets\arcade.PNG" className="img-responsive" style={{ width: "100%" }}
                        alt="Image" />
                        <h2>Retro Times</h2>
                        <p>
                            Hacklahoma 2021 was inspired by the growth of technology and how times have changed since the "retro" era. The tech community has made large bounds since its early days and we can all learn from the retro days.
                        </p>

                        <h2>Retro D&D</h2>
                        <p>
                            Dungeons & Dragons, or D&D, is a fantasy game that was designed by Gary Gygax and Dave Arneson. It was originally published in 1974 and has gone through five editions since then! A Dungeon Master guides players on epic adventures. The play style and format of the rules have changed since 1974, but the heart of the game remains the same and its popularity has only grown!
                        </p>

                        <h2>Retro Tech</h2>
                        <p>
                            Moore's law is an observation and prediction stating that the number of transistors on an integrated circuit double almost every two years. This rapid growth of technology has resulted in changes from computers the size of rooms to arcades and personal computers to smartphones. This technology continues to grow and soon we too will be retro!
                        </p>
                    </div>
                </div>
            </div>
        );
    }
}