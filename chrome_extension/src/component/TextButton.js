import React from 'react';
import "../style/button.css";

const TextButton = ({ title, onClick, login}) => {
  return (
    <span className={login ? "loginbutton":"textbutton" } onClick={onClick}>
      {title}
    </span>
  );
};

export default TextButton;