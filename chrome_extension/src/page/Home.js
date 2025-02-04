import React, { useState, useEffect }  from 'react';
import Logo from '../component/Logo'

function Home() {
  const [state, setState]=useState(<h4>로그인 후 서비스를 선택해보세요!</h4>)

  useEffect(() => {
    chrome.storage.local.get("user_id", (result)=>{
      if (result.user_id){
        setState(<h4>하단 메뉴의 서비스를 선택해보세요!</h4>)
      }
    });
  }, []);

  return (
    <div>
      <Logo />
      <h4>자기소개서 관리 서비스입니다!</h4>
      {state}
    </div>
  );
}

export default Home;
