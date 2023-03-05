import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import ConnectFourContainer from "./components/ConnectFourContainer";

const root = ReactDOM.createRoot(
  document.querySelector("body") as HTMLElement
);

root.render(
  <React.StrictMode>
    <ConnectFourContainer />
  </React.StrictMode>
);
