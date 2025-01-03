import React from 'react';
import Logo from '../component/Logo'

function Home() {
  return (
    <div>
      <div>
        <Logo />
      </div>
      <h4>자기소개서 관리 서비스입니다!</h4>
      <h4>현재 페이지에서 자기소개서를 탐색하거나 저장된 자기소개서를 불러올 수 있습니다.</h4>
      <h4>하단 메뉴에서 원하는 서비스를 선택해보세요!</h4>
    </div>
  );
}

export default Home;
