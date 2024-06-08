import React from "react";
import "./scanner.css";

const Scanner = () => {
  return (
    <div className="sql__scanner" id="scanner">
      <div className="sql__scanner-content">
        <div className="sql__scanner-header">
          <p>SQL SCANNER</p>
        </div>
        <div className="sql__scanner-input">
          <input
            type="text"
            placeholder="Enter your websit URL"
            className="sql__scanner-input-link"
          />
          <button type="button" className="sql__scanner-input-button">
            SCAN
          </button>
        </div>
      </div>
    </div>
  );
};

export default Scanner;
