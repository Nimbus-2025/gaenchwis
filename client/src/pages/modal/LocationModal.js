import React, { useState } from 'react';

const locations = {
    서울: ['강남구', '강동구', '강북구', '강서구', '관악구', 
        '광진구', '구로구', '금천구', '노원구', '도봉구', 
        '동대문구', '동작구', '마포구', '서대문구', '서초구', 
        '성동구', '성북구', '송파구', '양천구', '영등포구', 
        '용산구', '은평구', '종로구', '중구', '중랑구'
    ],
    경기도: ['고양시', '구리시', '군포시', '김포시', '남양주시', 
        '동두천시', '부천시', '성남시', '수원시', '시흥시', 
        '안산시', '안양시', '오산시', '용인시', '의왕시', 
        '의정부시', '파주시', '평택시', '하남시', '화성시'
    ],
    인천: [ '남동구', '부평구', '계양구', '미추홀구', '연수구', 
        '송도구', '중구', '옹진군'],
//     강원도: ['강릉시', '동해시', '속초시', '원주시', '춘천시', 
//         '태백시', '평창군', '홍천군', '횡성군', '영월군', 
//         '정선군', '철원군', '인제군', '양구군', '양양군', 
//         '고성군', '삼척시'
//     ],
//     충북: [
//         '청주시', '충주시', '제천시', '보은군', '옥천군', 
//         '영동군', '증평군', '진천군', '괴산군', '음성군', 
//         '단양군'
//     ],
//     충남: [
//         '천안시', '공주시', '보령시', '아산시', '서산시', 
//         '논산시', '계룡시', '당진시', '홍성군', '예산군', 
//         '태안군', '서천군', '청양군', '금산군', '부여군', 

//     ],
//     세종: [
//         '세종시' // 세종시는 단일 항목으로 추가
//     ],
//     대전: [
//         '동구', '중구', '서구', '유성구', '대덕구' // 대전시의 구들
//     ],
//     부산: [
//         '강서구', '금정구', '기장군', '남구', '동구', 
//         '부산진구', '북구', '사상구', '사하구', '서구', 
//         '수영구', '연제구', '영도구', '중구', '해운대구'
//     ],
//     울산: [
//         '남구', '동구', '북구', '중구', '울주군'
//     ],
//     대구: [
//         '남구', '달서구', '달성군', '동구', '북구', 
//         '서구', '수성구', '중구'
//     ],
//     경북: [
//         '포항시', '경주시', '안동시', '구미시', '영주시', 
//         '영천시', '상주시', '문경시', '칠곡군', '고령군', 
//         '성주군', '청도군', '봉화군', '울진군', '울릉군'
//     ],
//     경남: [
//         '창원시', '김해시', '진주시', '양산시', '사천시', 
//         '밀양시', '거제시', '통영시', '남해군', '하동군', 
//         '산청군', '함양군', '거창군', '합천군'
        
//     ],
//     광주: [
//         '광산구', '남구', '동구', '북구', '서구'
//     ],
//     전북: [
//         '전주시', '익산시', '군산시', '남원시', '정읍시', 
//         '김제시', '완주군', '진안군', '무주군', '장수군', 
//         '임실군', '순창군', '고창군', '부안군'
//     ],
//     전남: [
//         '광주시', '목포시', '여수시', '순천시', '나주시', 
//         '담양군', '곡성군', '구례군', '고흥군', '보성군', 
//         '화순군', '장흥군', '강진군', '해남군', '영암군', 
//         '무안군', '신안군'
//     ],
//     제주: ['제주시', '서귀포시'],
};

const LocationModal = ({ isOpen, onClose, onSelect, onApply }) => {
    const [selectedLocations, setSelectedLocations] = useState([]); // 선택된 시, 도 상태
    const [selectedDistricts, setSelectedDistricts] = useState({}); // 선택된 지역구 상태

    if (!isOpen) return null;

    const handleLocationClick = (location) => {
        setSelectedLocations((prev) => {
            if (prev.includes(location)) {
                return prev.filter((loc) => loc !== location); // 이미 선택된 경우 제거
            } else {
                return [...prev, location]; // 새로 선택된 경우 추가
            }
        });
    };

    const handleDistrictChange = (location, district) => {
        setSelectedDistricts((prev) => {
            const currentDistricts = prev[location] || [];
            if (currentDistricts.includes(district)) {
                return {
                    ...prev,
                    [location]: currentDistricts.filter(d => d !== district), // 체크 해제
                };
            } else {
                return {
                    ...prev,
                    [location]: [...currentDistricts, district], // 체크 추가
                };
            }
        });
    };
    const handleApply = () => {
        onApply(selectedLocations, selectedDistricts); // 선택된 지역과 지역구 전달
        onClose(); // 모달 닫기
    };


    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxHeight: '70vh', overflowY: 'auto' }}>
                <h2>지역 선택</h2>
                <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', marginBottom: '20px' }}>
                    {Object.keys(locations).map((location) => (
                        <div key={location} style={{ width: '60%', marginBottom: '10px' }}>
                            <h3 onClick={() => handleLocationClick(location)} style={{ cursor: 'pointer' }}>
                                {location} {selectedLocations.includes(location) ? '✔️' : ''}
                            </h3>
                            {selectedLocations.includes(location) && ( // 선택된 시도일 때 지역구 표시
                                <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                                    {locations[location].map((district, index) => (
                                        <div key={`${district}-${index}`} style={{
                                            flexBasis: 'calc(30% - 10px)', // 한 열에 5개씩 표시 (20% 크기 - 간격)
                                            padding: '5px',
                                        }}>
                                            <label>
                                                <input
                                                    type="checkbox"
                                                    checked={!!(selectedDistricts[location] && selectedDistricts[location].includes(district))} // 체크 상태
                                                    onChange={() => handleDistrictChange(location, district)} // 체크박스 변경 핸들러
                                                />
                                                {district}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
                <button onClick={handleApply}>적용</button> {/* 적용 버튼 */}
                <button onClick={onClose}>닫기</button>
            </div>
        </div>
    );
};

export default LocationModal;