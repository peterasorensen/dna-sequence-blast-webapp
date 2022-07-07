import React, {useState} from "react";
import InputModal from "./InputModal";
import OutputModal from "./OutputModal";

const MainScreen = () => {
  const [queriesShouldUpdate, setQueriesShouldUpdate] = useState(false);
  return (
    <div className='container'>
      <InputModal queriesShouldUpdate={queriesShouldUpdate} setQueriesShouldUpdate={setQueriesShouldUpdate}/>
      <OutputModal queriesShouldUpdate={queriesShouldUpdate}/>
    </div>
  )
};

export default MainScreen;
