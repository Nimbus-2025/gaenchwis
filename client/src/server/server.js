const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { OAuth2Client } = require('google-auth-library');

const app = express();
const PORT = 5000;
const client = new OAuth2Client('800144464912-bjdvo0b4vru9sp0i1segrktsgbk9kngu.apps.googleusercontent.com'); // 구글 클라이언트 ID를 여기에 입력하세요

// 미들웨어 설정
app.use(cors());
app.use(bodyParser.json());

// 기본 GET 요청 핸들러
app.get('/', (req, res) => {
  res.send('Hello World');
});

// 구글 인증 엔드포인트
app.post('/auth/google', async (req, res) => {
  const { credential } = req.body;

  try {
    const ticket = await client.verifyIdToken({
      idToken: credential,
      audience: '800144464912-bjdvo0b4vru9sp0i1segrktsgbk9kngu.apps.googleusercontent.com', // 구글 클라이언트 ID를 여기에 입력하세요
    });
    const payload = ticket.getPayload();
    console.log('User data:', payload);

    // 사용자 정보를 처리하는 로직을 여기에 추가합니다.
    // 예를 들어, 데이터베이스에 사용자 정보를 저장하거나 세션을 생성할 수 있습니다.

    res.status(200).json({ message: 'Google login successful', user: payload });
  } catch (error) {
    console.error('Error verifying Google token:', error);
    res.status(401).json({ message: 'Invalid token' });
  }
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});