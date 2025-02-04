import React from 'react';
import TextButton from './TextButton';
import "../style/background.css";
import HomeImage from "../image/home.png";
import PostImage from "../image/post.png";
import EssayImage from "../image/essay.png";
import "../style/background.css";
import "../style/icon.css";


function Footer() {
  return (
    <div className="div">
      <div className="footer-div" onClick={ () => { 
        chrome.runtime.sendMessage({ message: 'page_main' }); 
      }}>
        <img src={HomeImage} className="footer-icon" />
        <TextButton
          title="Home"
        />
      </div>
      <div className="footer-div" onClick={ () => { 
        chrome.runtime.sendMessage({ message: 'page_detectpost' }); 
      }}>
        <img src={PostImage} className="footer-icon" />
        <TextButton
          title="Post"
        />
      </div>
      <div className="footer-div" onClick={ () => {
        chrome.runtime.sendMessage({ message: 'page_loadessay' });
      }}>
        <img src={EssayImage} className="footer-icon" />
        <TextButton
          title="Essay"
        />
      </div>
      
    </div>
  );
}

export default Footer;