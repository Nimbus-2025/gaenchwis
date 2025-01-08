const express = require('express');
const mongoose = require('mongoose');
const app = express();

// MongoDB 연결 (MongoDB Atlas를 사용할 경우, Atlas URL을 사용해야 함)
mongoose.connect('mongodb://localhost:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => {
  console.log('MongoDB 연결 성공!');
}).catch((err) => {
  console.error('MongoDB 연결 실패:', err);
});

app.get('/', (req, res) => {
  res.send('Hello from the backend!');
});

const port = 5001;
app.listen(port, () => {
  console.log(`서버가 ${port} 포트에서 실행 중...`);
});