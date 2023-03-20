import './css/styles.css'
import {Route, BrowserRouter, Routes} from "react-router-dom";
import React from "react";
import AuthPage from "./auth_page";

function App() {

  return (
      <BrowserRouter>
    <div className="App">
      <Routes>
        <Route path="/auth" element={<AuthPage/>}></Route>
      </Routes>
    </div>
      </BrowserRouter>
  );
}

export default App;