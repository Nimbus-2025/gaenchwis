import React from 'react';
import LogoImage from '../logo.png'
import '../style/logo.css'

function Logo() {
  return (
    <div>
      <a href="https://gaenchwis.click" 
        target="_blank" 
        rel="noopener noreferrer"
        className="logo-href"
      >
        <img src={LogoImage} className="logo" alt="logo" />
      </a>
    </div>
  );
}

export default Logo;