const mongoose = require('mongoose');

// 사용자 스키마 정의
const userSchema = new mongoose.Schema({
    googleId: { type: String, required: true }, // 구글 ID
    name: { type: String, required: true }, // 사용자 이름
    email: { type: String, required: true }, // 사용자 이메일
});

// User 모델 생성
const User = mongoose.model('User', userSchema);

// User 모델을 내보냄
module.exports = User;