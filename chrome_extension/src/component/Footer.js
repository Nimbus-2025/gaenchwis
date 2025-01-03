import React from 'react';
import Button from './Button';

function Footer() {
  return (
    <div>
      <Button
        title="Home"
        onClick={ () => { 
          chrome.runtime.sendMessage({ message: 'page_main' }); 
        }}
      />
      <Button
        title="Save Essay"
        onClick={ () => { 
          chrome.runtime.sendMessage({ message: 'page_detectessay' }); 
        }}
      />
      <Button
        title="Load Essay"
        onClick={ () => {
          chrome.runtime.sendMessage({ message: 'page_loadessay' });
        }}
      />
    </div>
  );
}

export default Footer;