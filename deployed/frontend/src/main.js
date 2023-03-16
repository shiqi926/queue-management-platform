import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
// Firebase App (the core Firebase SDK) is always required and
// must be listed before other Firebase SDKs
import firebase from "firebase/app"

// Add the Firebase services that you want to use
import "firebase/auth";
//import "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyB6kh4BWE0_pOf165R3O146n087W4C4qyQ",
    authDomain: "esd-g9t7.firebaseapp.com",
    projectId: "esd-g9t7",
    storageBucket: "esd-g9t7.appspot.com",
    messagingSenderId: "453611533955",
    appId: "1:453611533955:web:1f4ed252f2ba58b1580db6",
    measurementId: "G-0XS04KMQZF"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
//const firebaseAuth = firebase.auth();

// var displayName = user.displayName;
// var email = user.email;
// var uid = user.uid;

const app = createApp(App).use(router).mount('#app')

export default {firebaseApp, app}
