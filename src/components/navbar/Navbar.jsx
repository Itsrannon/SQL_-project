import React, { useState } from "react";
import "./navbar.css";
import { RiMenu3Line, RiCloseLine } from "react-icons/ri";
import Assets1 from "../../assets/Asset 1.png";

const Menu = () => (
  <>
    <p>
      <a href="#home">Home</a>
    </p>
    <p>
      <a href="#Ai">Ai</a>
    </p>
    <p>
      <a href="#scanner">Scanner</a>
    </p>
  </>
);
const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);
  return (
    <div className="sql__navbar">
      <div className="sql__navbar-links">
        <div className="sql__navbar-links-logo">
          <img src={Assets1} alt="logo" />
        </div>
        <div className="sql__navbar-links-container">
          <Menu />
        </div>
      </div>
      <div className="sql__navbar-sign">
        <button type="button">Sign in </button>
        <button type="button">Sign up</button>
      </div>
      <div className="sql__navbar-menu">
        {toggleMenu ? (
          <RiCloseLine
            color="#000"
            size={27}
            onClick={() => setToggleMenu(false)}
          />
        ) : (
          <RiMenu3Line
            color="#000"
            size={27}
            onClick={() => setToggleMenu(true)}
          />
        )}

        {toggleMenu && (
          <div className="sql__navbar-menu-container scale-up-center">
            <div className="sql__navbar-menu-container-links">
              <Menu />

              <div className="sql__navbar-menu-container-links-sign">
                <p className="signing_p">Sign in</p>
                <button type="button">Sign up</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
