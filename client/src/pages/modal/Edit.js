import React from 'react';
import './Modal.css'; // 스타일을 위한 CSS 파일

const Modal = ({ isOpen, onClose, onSave, phoneNumber, setPhoneNumber }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>전화번호 입력</h2>
                <label>
                    전화번호:
                    <input
                        type="text"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                </label>
                <button onClick={onSave}>저장</button>
                <button onClick={onClose}>닫기</button>
            </div>
        </div>
    );
};

export default Modal;