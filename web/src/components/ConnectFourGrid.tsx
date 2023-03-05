import "../css/ConnectFourGrid.css"
import "../css/Column.css"
import React, {useEffect, useState} from "react";
import * as tf from '@tensorflow/tfjs';

function Hole(

    props : {
        player: number
    }

    ) {

    if (props.player === 1) {
        return <div className="Column-holeContainer one"></div>;
    }

    else if (props.player === 2) {
        return <div className="Column-holeContainer two"></div>;
    }

    else {
        return <div className="Column-holeContainer"></div>;
    }

}

function Column(

    props : {
        columnState : Array<number>,
        clickHandler : () => any
    }

    ) {

    return (

        <div onClick={() => props.clickHandler()} className="Column-container">
            {props.columnState.map((h, i) => <Hole key={i} player={h}/>)}
        </div>

    );

}

let d = [0, 0, 0, 0, 0, 0]

const ConnectFourGrid = (

    props : {
        model : any
    }

    ) => {

    const [currentTurn, setCurrentTurn] = useState<number>(1);
    const [columnState, setColumnState] = useState<Array<Array<number>>>([d, d, d, d, d, d, d]);

    useEffect(() => {

        if (currentTurn === 2) {
            console.log("AI");

            let board = tf.tensor2d(columnState)
            board = board.reshape([1, 6, 7, 1])
            let ws = props.model.predict(board).dataSync();
            let n = ws.indexOf(Math.max(...ws));

            console.log(n);

            let newState = JSON.parse(JSON.stringify(columnState));

            let j = 0;

            while (newState[n][j] === 0) {
                j++;
            }

            newState[n][j - 1] = currentTurn;

            console.log(n);

            setColumnState(newState)
            setCurrentTurn(1)
        }

    }, [currentTurn]);

    return (

        <div className="ConnectFourGrid-container">

            {columnState.map((c, i) => <Column key={i} clickHandler={() => {

                console.log("ME");

                let newState : Array<Array<number>> = JSON.parse(JSON.stringify(columnState));

                let j = 0;

                while (newState[i][j] === 0) {
                    j++;
                }

                newState[i][j - 1] = currentTurn;

                console.log(i);

                setColumnState(newState)
                setCurrentTurn(2)

            }

            } columnState={c}/>)}

        </div>

    );

}

export default ConnectFourGrid;