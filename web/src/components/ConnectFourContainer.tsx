import ConnectFourGrid from "./ConnectFourGrid";
import "../css/ConnectFourContainer.css"
import React, {useEffect, useState} from "react";
import * as tf from '@tensorflow/tfjs';

const ConnectFourContainer = () => {

    const [model, setModel] = useState<any>(undefined);

    async function loadModel(url: any) {

        try {
            console.log(`${url}`)
            const model = await tf.loadGraphModel(`${url}`);
            setModel(model);
            console.log("Load model success")
        }

        catch (err) {
            console.log(err);
        }

    }

    useEffect(()=>{

        tf.ready().then(()=>{
            loadModel("winner-js/model.json")
        });

    },[])

    return (

        <div className="ConnectFourContainer-container">
            <div className="ConnectFourContainer-title">JHCONNECT</div>
            <ConnectFourGrid model={model}/>
        </div>

    );

}

export default ConnectFourContainer;