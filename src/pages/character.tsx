import React from 'react';
import GlobalState from '../global_state'

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
        let abilityids: string[] = ['str', 'int', 'dex', 'wis', 'con', 'cha'];
        let abilityList: any[] = abilities.map((ability, index: number) =>
            <div className="col-xs-6" key={ability}>
                <div className="panel panel-warning">
                    <div className="panel-heading">{ability}</div>
                    <div className="panel-body">
                        <div className="panel panel-warning">
                            <div className="panel-body">+{GlobalState.mod_from_total(GlobalState.player_character.abilities[abilityids[index]])}</div>
                        </div>

                        <div className="panel panel-warning">
                            <div className="panel-body">{GlobalState.player_character.abilities[abilityids[index]]}</div>
                        </div>
                    </div>
                </div>
            </div>);

        let skills: string[] = ['Acrobatics', 'Animal handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'];
        let skillids: string[] = ['acrobatics', 'animal_handling', 'arcana', 'athletics', 'deception', 'history', 'insight', 'intimidation', 'investigation', 'medicine', 'nature', 'perception', 'performance', 'persuasion', 'religion', 'sleight_of_hand', 'stealth', 'survival'];
        let bonusList: any[] = skills.map((skill, index) =>
            <div className="row" key={skill}>
                <div className="panel panel-warning col-xs-6">
                    <div className="panel-body">{skill}</div>
                </div>
                <div className="panel panel-warning col-xs-6">
                    <div className="panel-body">{GlobalState.player_character.skill_bonuses[skillids[index]]}</div>
                </div>
            </div>);

        return (
            <div>
                <div className="container">
                    <div className="row">
                        <div className="col-xs-12 mx-auto">
                            <div className="panel">
                                <div id="charName" className="panel-heading ">{GlobalState.player_character.name}</div>
                                <div id="charPic" className="panel-body"><img className="mx-auto d-block" src={GlobalState.player_character.avatar_url}
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