import React from "react";
import { Home, Navbar, Scanner, Header } from "./components";
import "./App.css";
const App = () => {
  return (
    <div className="container">
      <Navbar />
      <Home />
      <Header />
      <Scanner />
    </div>
  );
};

export default App;
