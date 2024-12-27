import firebase from 'firebase/app';
import 'firebase/firestore';

const firebaseConfig = {
  // Firebase 설정 정보를 여기에 넣으세요
  apiKey: "your-api-key",
  authDomain: "your-auth-domain",
  projectId: "your-project-id",
  storageBucket: "your-storage-bucket",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};

// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export const firestore = firebase.firestore();
export const scheduleCollection = firestore.collection('schedule');