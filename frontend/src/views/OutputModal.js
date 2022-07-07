import React from "react";
import ResultOutput from "../modules/ResultOutput";

const OutputModal = ({queriesShouldUpdate}) => {
  return (
    <div className="app">
      <ResultOutput queriesShouldUpdate={queriesShouldUpdate}/>
    </div>
  )
};

export default OutputModal;
