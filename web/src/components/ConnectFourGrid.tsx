import "../css/ConnectFourGrid.css"
import "../css/Column.css"
import React from "react";

function Hole() {
    return <div className="Column-holeContainer"></div>;
}

function Column(

    props : {
        columnState : Array<number>
    }

    ) {

    return (

        <div className="Column-container">
            <Hole />
            <Hole />
            <Hole />
            <Hole />
            <Hole />
            <Hole />
        </div>

    );

}

const ConnectFourGrid = (

    props : {
        columnStates : Array<Array<number>>
    }

    ) => {

    return (

        <div className="ConnectFourGrid-container">
            {props.columnStates.map(c => <Column columnState={c}/>)}
        </div>

    );

}

export default ConnectFourGrid;