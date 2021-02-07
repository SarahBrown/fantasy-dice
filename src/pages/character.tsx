import React from 'react';

interface IProps {

}

interface IState {

}

export default class Character extends React.Component<IProps, IState> {

    constructor(props: any) {
        super(props);
        this.state = {};
    }

    render() {
        let abilities: string[] = ['Strength', 'Intelligence', 'Dexterity', 'Wisdom', 'Constitution', 'Charisma'];
        let abilityList: any[] = abilities.map((ability) =>
            <div className="col-xs-6">
                <div className="panel panel-warning">
                    <div className="panel-heading">{ability}</div>
                    <div className="panel-body">
                        <div className="panel panel-warning">
                            <div className="panel-body">MOD</div>
                        </div>

                        <div className="panel panel-warning">
                            <div className="panel-body">RAW</div>
                        </div>
                    </div>
                </div>
            </div>);

        let skills: string[] = ['Acrobatics', 'Animal handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of hand', 'Stealth', 'Survival'];
        let bonusList: any[] = skills.map((skill) =>
            <div className="row">
                <div className="panel panel-warning col-xs-6">
                    <div className="panel-body">{skill}</div>
                </div>
                <div className="panel panel-warning col-xs-6">
                    <div className="panel-body">MOD</div>
                </div>
            </div>);

        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="col-xs-12 mx-auto">
                            <div className="panel">
                                <div id="charName" className="panel-heading ">Character Name</div>
                                <div id="charPic" className="panel-body"><img className="mx-auto d-block" src="assets\profilePic1.PNG"
                                    style={{ width: "50%" }} alt="Image" /></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="container">
                    <div className="col text-center">
                        <button data-toggle="collapse" data-target="#mod" className="btn-collapse">Modifiers</button>
                    </div>
                    <br />

                    <div id="mod" className="row">
                        {abilityList}
                    </div>
                </div>

                <br />
                <div className="container">
                    <div className="col text-center">
                        <button data-toggle="collapse" data-target="#bonusSkill" className="btn-collapse">Skill Bonuses</button>
                    </div>
                    <br />

                    <div id="bonusSkill" className="panel-collapse collapse">
                        {bonusList}
                    </div>
                </div>

            </div>

        );
    }
}