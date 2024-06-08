import React from "react";
import "./header.css";
import Asset5 from "../../assets/Asset 5.png";

const Header = () => {
  return (
    <div className="sql__main" id="Ai">
      <div className="aql__main-content">
        <p>
          HI MY
          <span> NAME IS </span>
          <span> RIFT </span>
        </p>
      </div>
      <div className="sql__main-img">
        <img src={Asset5} alt="" />
      </div>
    </div>
  );
};

export default Header;
