// src/component/calendar1/Firebase.js

import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,           // 실제 API 키
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,   // 실제 인증 도메인
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,     // 실제 프로젝트 ID
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

// Firebase 초기화가 한 번만 실행되도록 보장
let app;
try {
  app = initializeApp(firebaseConfig);
} catch (error) {
  if (!/already exists/.test(error.message)) {
    console.error('Firebase initialization error:', error);
  }
}

const db = getFirestore(app);

export { app, db };