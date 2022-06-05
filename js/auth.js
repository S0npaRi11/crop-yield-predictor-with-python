import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.8.2/firebase-auth.js";
import { auth } from './firebaseInit.js'

//listen to auth status changes
auth.onAuthStateChanged(user => {
    if(user){
        console.log('user logged in : ', user)
        sessionStorage.setItem('logged', 'loggedIn')
    }else {
        console.log('user logged out')
    }
})

// registration form
const regForm = document.querySelector('#registrationForm')
if(regForm){
    regForm.addEventListener('submit', (e) => {
        e.preventDefault()
        
        const name = regForm['name'].value
        const email = regForm['email'].value
        const password = regForm['password'].value

        createUserWithEmailAndPassword(auth,email,password).then(cred => {
            regForm.reset()
            window.location = './index.html'
        }).catch(error => {
            console.log(error)
            alert('Error while creating new user.')
        })
    })
}

// login form
const loginForm = document.querySelector('#loginForm')
if(loginForm){
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault()

        const email = loginForm['email'].value
        const password = loginForm['password'].value

        signInWithEmailAndPassword(auth, email, password).then(cread => {
            loginForm.reset()
            window.location = './index.html'
        }).catch(error => {
            alert(error.code + '\n' + error.message)
        })
    })
}

const logout = document.querySelector('#logout')
if(logout){
    logout.addEventListener('click', (e) => {
        e.preventDefault()
        sessionStorage.removeItem('logged')
        auth.signOut()
        window.location.href = './login.html'
    })
}
