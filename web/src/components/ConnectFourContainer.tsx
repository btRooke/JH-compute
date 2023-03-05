import ConnectFourGrid from "./ConnectFourGrid";
import "../css/ConnectFourContainer.css"
import React from "react";

const d = [0, 0, 1, 2, 0, 1];

const ConnectFourContainer = () => {

    return (

        <div className="ConnectFourContainer-container">
            <div className="ConnectFourContainer-title">JHCONNECT</div>
            <ConnectFourGrid columnStates={[d, d, d, d, d, d, d]}/>
        </div>

    );

}

export default ConnectFourContainer;