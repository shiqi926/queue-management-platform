<template>
    <form id = "adminlogin" @submit.prevent="login"> 
        <i class="bi bi-person-fill"></i>
        <h1 class="card-title display-4">Admin Login</h1>
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
    name: 'AdminLogin',
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
                if (userID == "48e6aimiq3VNF45VylXA6UAVODd2" || userID == "XiV2CwmCzqUCFxJCjxuGpDPUzMY2"){
                    this.store.apiKey = "AIzaSyABlb3ALz9Ylq0NWkxKmzBh6GI1Pjcc_RM";
                    this.$router.push('/panel');
                }
                else{
                    alert("Wait a second... You're not the admin! Stop trying to hack into the system, Mr Robot.")
                    this.$router.push('/');
                }
            })
            .catch(error => {
                alert(error.message);
            });
        },
    }
}
</script>