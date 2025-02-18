import React, { useState } from 'react';
import './Modal.css'; // 스타일을 위한 CSS 파일

const Edit = ({ isOpen, onClose, onSave, name, email, phone}) => {
    const [editphone, setEditPhone]=useState(phone);
    const [editemail, setEditEmail]=useState(email);
    const [editname, setEditName]=useState(name);

    if (!isOpen) return null;

    return (
        <div className="edit-modal-overlay">
            <div className="edit-modal-content">
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
                <div className="edit-modal-buttons">
                    <button onClick={()=>{
                        onSave(editname,editemail,editphone);
                        onClose();
                    }}>저장</button>
                    <button onClick={onClose}>닫기</button>
                </div>
            </div>
        </div>
    );
};

export default Edit;