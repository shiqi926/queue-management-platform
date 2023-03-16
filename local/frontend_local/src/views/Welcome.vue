<template>
    <div class="welcome bg">
        <div class="container-fluid">
            <div class="row" style="height: 100vh;">
                <div class="col-sm-10 col-md-8 col-lg-6 mx-auto my-auto">
                    <div class="card bg-light" style="border-radius: 1.5rem;">
                        <div class="card-body">

                            <LoginForm v-if="logging&&!admin" />
                            <RegisterForm v-if="!logging&&!admin"/>
                            <AdminLogin v-if="admin"/>

                            <div class="m-4">
                                <button v-if="!admin" class = "btn btn-info mx-3" @click="logging=!logging">{{logging ? regMsg : logMsg}}</button>
                            </div>
                            <button class = "btn btn-link mx-3" @click="admin=!admin">{{admin ? userMsg : adminMsg}}</button>
                        </div>
                    </div>                    
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .bg {
        background: lightblue;
        width: 100vw;
        height: 100vh;
    }
</style>

<script>
// @ is an alias to /src
import RegisterForm from '@/components/RegisterForm.vue'
import LoginForm from '@/components/LoginForm.vue'
import AdminLogin from '@/components/AdminLogin.vue'

export default {
    name: 'Welcome',
    components: {
        RegisterForm,
        LoginForm,
        AdminLogin
    },
    data() {
        return{
            logging : true,
            regMsg: "Click here to register!",
            logMsg: "Click here to login!",
            admin: false,
            adminMsg: "Log in as admin",
            userMsg: "Log in as user"
        }
    }
}
</script>
