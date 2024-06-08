import React from "react";
import "./home.css";
import Asset3 from "../../assets/Asset 3.png";
const Home = () => {
  return (
    <div className="sql__header" id="home">
      <div className="sql__header-content">
        <h3 className="sql__header-content_ai">AI</h3>
        <div className="sql__header-img">
          <img src={Asset3} alt="" />
        </div>
        <div className="sql-scanner">
          <span className="sql">SQL</span>
          <span className="scanner">SCANNER</span>
          <div className="sql__header-block"></div>
          {/* <div className="additional-text">
            <span className="injection">INJECTION</span>
            <span className="year">2024</span>
          </div> */}
        </div>
      </div>
    </div>
  );
};

export default Home;
