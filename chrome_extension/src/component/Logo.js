import React from 'react';
import LogoImage from '../image/logo.png'
import '../style/logo.css'

function Logo() {
  return (
    <a href="https://gaenchwis.click" 
      target="_blank" 
      rel="noopener noreferrer"
      className="logo-href"
    >
      <img src={LogoImage} className="logo" alt="logo" />
    </a>
  );
}

export default Logo;