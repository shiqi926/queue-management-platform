<template>
    <form id = "loginform" @submit.prevent="login"> 
        <h1 class="card-title display-4">Login</h1>
        <hr class="my-4">
        <div class="form-group">       
            <label for="loginEmail">Email Address</label>     
            <input class="form-control" id ="loginEmail" type="email" placeholder="Enter your email address" v-model="email"/>
        </div>

        <div class="form-group">
            <label for="loginPW">Password</label>       
            <input class="form-control" id ="loginPW" type="password" placeholder="Enter your password" v-model="password"/> 
        </div>    

        <button type="submit" class="btn btn-info">
            Login
        </button>
    </form>
</template>



<script>

import firebase from 'firebase'

export default {
    name: 'LoginForm',
    inject: ["store"],
    data(){
        return{
        email: "",
        password: "",
        name: "" 
        }
    },
    methods: {
        login() {
            firebase
            .auth()
            .signInWithEmailAndPassword(this.email, this.password)
            .then((userCredential) => {
                var dName = userCredential.user.displayName;
                var userID = userCredential.user.uid;
                this.store.username = dName;
                this.store.uid = userID;
                alert(`Successfully logged in. Welcome, ${this.store.username}!`);
                this.$router.push('/gallery');
            })
            .catch(error => {
                alert(error.message);
            });
        },
    }
}
</script>