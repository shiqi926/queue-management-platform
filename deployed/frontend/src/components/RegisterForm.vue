<template>
    <form @submit.prevent="register(this.name)"> 
        <h1 class="card-title display-4">Register</h1>
        <hr class="my-4">
        <div class="form-group">       
            <label for="regEmail">Email Address</label>     
            <input class="form-control" id ="regEmail" type="email" placeholder="Enter your email address" v-model="email"/>
        </div>
        <div class="form-group">   
            <label for="regPW">Password</label>    
            <input class="form-control" id="regPW" type="password" placeholder="Enter your password" v-model="password"/> 
            <small id="passwordWarning" class="form-text text-muted">Please don't use your actual real-life password</small>
        </div>    
        <div class="form-group"> 
            <label for="regName">Name</label>    
            <input class="form-control" type="text" placeholder="Your Name" v-model="name"/> 
        </div>
        <button type="submit" class="btn btn-info">
            Register
        </button>  
    </form>
</template>

<script>
import firebase from "firebase";

export default {
    name: 'RegisterForm',
    inject: ["store"],
    data(){
        return{
            email: "",
            password: "",
            name: ""
        }
    },

    methods: {
        register(name) {
            firebase
            .auth()
            .createUserWithEmailAndPassword(this.email, this.password)
            .then((userCredential)=>{
                var user = userCredential.user;
                this.store.uid = user.uid;
                this.store.username = name;
                this.addToCustomersDB();
            })
            .then(()=>{
                var user = firebase.auth().currentUser;
                user.updateProfile({
                    displayName: this.store.username
                });
                alert(`Successfully registered! Welcome, ${this.store.username}.`);
                this.$router.push('/gallery');
            })
            .catch(error=>{
                alert(error.message);
            })  
        },
        
        async addToCustomersDB(){
            // var customersURL = "http://127.0.0.1:5000/customers/add";
            // var customersURL = "https://themepark-5sdwlfnn.uc.gateway.dev/register";
            var customersURL = "https://customers-wy3g4hhdja-uc.a.run.app/customers/add";
            try {
                var reqbody = JSON.stringify({
                    "email": this.email,
                    "password": this.password,
                    "currentAttraction": "",
                    "name": this.store.username,
                    "cid": this.store.uid
                });
                console.log(reqbody);
                const response = await fetch(customersURL, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: reqbody
                    });
                console.log(response);
                const result = await response.json();
                if (result.code === 201){
                    console.log("New customer added to customers DB")
                }
                console.log(result);
            } catch(error){
                console.log(error);
            }

        }
    },
}
</script>