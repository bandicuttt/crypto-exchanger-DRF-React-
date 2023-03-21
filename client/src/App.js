import './css/styles.css'
import {Route, BrowserRouter, Routes} from "react-router-dom";
import React, {useState} from "react";
import AuthPage from "./auth_page";
import OrderPage from "./order_page";

function App() {
  return (
      <BrowserRouter>
    <div className="App">
      <Routes>
        <Route path="/auth" element={<AuthPage/>}></Route>
        <Route path="/orders" element={<OrderPage/>}></Route>
      </Routes>
    </div>
      </BrowserRouter>
  );
}

export default App;