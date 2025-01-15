import React, { useState } from 'react';
import './Modal.css'; // 스타일을 위한 CSS 파일

const Modal = ({ isOpen, onClose, onSave }) => {
    const [editphone, setEditPhone]=useState("")
    const [editemail, setEditEmail]=useState("")
    const [editname, setEditName]=useState("")

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>프로필 수정</h2>
                <label>
                    이름:
                    <input
                        type="text"
                        value={editname}
                        onChange={(e) => setEditName(e.target.value)}
                    />
                </label>
                <label>
                    전화번호:
                    <input
                        type="text"
                        value={editphone}
                        onChange={(e) => setEditPhone(e.target.value)}
                    />
                </label>
                <label>
                    이메일:
                    <input
                        type="text"
                        value={editemail}
                        onChange={(e) => setEditEmail(e.target.value)}
                    />
                </label>
                <button onClick={()=>{
                    onSave(editname,editemail,editphone);
                    onClose();
                }}>저장</button>
                <button onClick={onClose}>닫기</button>
            </div>
        </div>
    );
};

export default Modal;