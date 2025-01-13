import React from 'react';
import "../style/button.css";

const TextButton = ({ title, onClick}) => {
  return (
    <span className={title==="Login" ? "loginbutton":"textbutton" } onClick={onClick}>
      {title}
    </span>
  );
};

export default TextButton;