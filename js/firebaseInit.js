  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.2/firebase-app.js";
  import { getAuth } from "https://www.gstatic.com/firebasejs/9.8.2/firebase-auth.js";
  import keys from './keys.js'
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: keys.FIREBASE_API_KEY,
    authDomain: keys.FIREBASE_AUTH_DOMAIN,
    projectId: keys.FIREBASE_PROJECT_ID,
    storageBucket: keys.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: keys.FIREBASE_MESSAGING_SENDER_ID,
    appId: keys.FIREBASE_APP_ID
  };

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app)
