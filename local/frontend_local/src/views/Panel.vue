<template>
    <div class="about bg">
        <div class="jumbotron jumbotron-fluid mb-3 bg-light">
            <div class="container">
                <h2 class="display-4">Hello, {{store.username}}!</h2>
                <p class="lead">Welcome to the Administrator Panel. 
                    <strong v-if="crowd==0">The virtual queues are currently empty. </strong > 
                    <strong v-if="crowd==1">There is {{crowd}} visitor in a virtual queue</strong> 
                    <strong v-if="crowd > 2">There are {{crowd}} visitors in the virtual queues now.</strong>
                </p>
                <div class ="row">
                    <div class = "d-flex align-items-center col-6 justify-content-start">
                        <button type="button float-left align-self-center" class="btn btn-outline-primary" @click="navToDashboard">View Dashboard</button>
                    </div>
                    <div class = "d-flex col-6 align-items-center justify-content-end">
                        <h5 class ="float-right align-self-center">NEA Weather Forecast: {{forecast}}
                            <svg v-if="thunder" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-lightning-rain" viewBox="0 0 16 16">
                                <path d="M2.658 11.026a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm9.5 0a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm-7.5 1.5a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm9.5 0a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm-.753-8.499a5.001 5.001 0 0 0-9.499-1.004A3.5 3.5 0 1 0 3.5 10H13a3 3 0 0 0 .405-5.973zM8.5 1a4 4 0 0 1 3.976 3.555.5.5 0 0 0 .5.445H13a2 2 0 0 1 0 4H3.5a2.5 2.5 0 1 1 .605-4.926.5.5 0 0 0 .596-.329A4.002 4.002 0 0 1 8.5 1zM7.053 11.276A.5.5 0 0 1 7.5 11h1a.5.5 0 0 1 .474.658l-.28.842H9.5a.5.5 0 0 1 .39.812l-2 2.5a.5.5 0 0 1-.875-.433L7.36 14H6.5a.5.5 0 0 1-.447-.724l1-2z"/>
                            </svg>
                            <svg v-if="rain" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-rain" viewBox="0 0 16 16">
                                <path d="M4.158 12.025a.5.5 0 0 1 .316.633l-.5 1.5a.5.5 0 0 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.317zm3 0a.5.5 0 0 1 .316.633l-1 3a.5.5 0 0 1-.948-.316l1-3a.5.5 0 0 1 .632-.317zm3 0a.5.5 0 0 1 .316.633l-.5 1.5a.5.5 0 0 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.317zm3 0a.5.5 0 0 1 .316.633l-1 3a.5.5 0 1 1-.948-.316l1-3a.5.5 0 0 1 .632-.317zm.247-6.998a5.001 5.001 0 0 0-9.499-1.004A3.5 3.5 0 1 0 3.5 11H13a3 3 0 0 0 .405-5.973zM8.5 2a4 4 0 0 1 3.976 3.555.5.5 0 0 0 .5.445H13a2 2 0 0 1 0 4H3.5a2.5 2.5 0 1 1 .605-4.926.5.5 0 0 0 .596-.329A4.002 4.002 0 0 1 8.5 2z"/>
                            </svg>
                            <svg v-if="cloud" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud" viewBox="0 0 16 16">
                                <path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.785 2.23 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.825 10.328 3 8 3a4.53 4.53 0 0 0-2.941 1.1z"/>
                            </svg>
                            <svg v-if="sun" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-sun" viewBox="0 0 16 16">
                                <path d="M7 8a3.5 3.5 0 0 1 3.5 3.555.5.5 0 0 0 .624.492A1.503 1.503 0 0 1 13 13.5a1.5 1.5 0 0 1-1.5 1.5H3a2 2 0 1 1 .1-3.998.5.5 0 0 0 .51-.375A3.502 3.502 0 0 1 7 8zm4.473 3a4.5 4.5 0 0 0-8.72-.99A3 3 0 0 0 3 16h8.5a2.5 2.5 0 0 0 0-5h-.027z"/>
                                <path d="M10.5 1.5a.5.5 0 0 0-1 0v1a.5.5 0 0 0 1 0v-1zm3.743 1.964a.5.5 0 1 0-.707-.707l-.708.707a.5.5 0 0 0 .708.708l.707-.708zm-7.779-.707a.5.5 0 0 0-.707.707l.707.708a.5.5 0 1 0 .708-.708l-.708-.707zm1.734 3.374a2 2 0 1 1 3.296 2.198c.199.281.372.582.516.898a3 3 0 1 0-4.84-3.225c.352.011.696.055 1.028.129zm4.484 4.074c.6.215 1.125.59 1.522 1.072a.5.5 0 0 0 .039-.742l-.707-.707a.5.5 0 0 0-.854.377zM14.5 6.5a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1h-1z"/>
                            </svg>
                        </h5>
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div v-for="attr in attractionsList" :key="attr">
                <QueueCard v-bind:attraction="attr"></QueueCard>
            </div>
        </div>
    </div>
</template>

<style>
    .bg {
        background: lightblue;
        width: 100vw;
        height: 150vh;
    }
</style>

<script>
//import firebase from "firebase";
import QueueCard from "@/components/QueueCard.vue"

export default {
    name: 'Gallery',
    data(){
        return{
            //userEmail: "",
            attractionsList: ["Viking Ship", "Rollercoaster", "Carousell"],
            crowd: 0,
            thunder: false,
            rain: false,
            cloud: false,
            sun: false,
            forecast: ""     
        }
    },
    inject: ['store'],
    components:{
        QueueCard
    },
    methods:{
        async getTotalCrowd(){
            var tcURL = "http://127.0.0.1:5001/attractions/all";
            // var tcURL = "https://themepark-5sdwlfnn.uc.gateway.dev/crowd?key=" + this.store.apiKey;
            try {
                const response = await fetch(
                    tcURL,{
                        method: "GET",
                        // headers: {"Content-Type": "application/json"}
                    });
                const result = await response.json();
                if (result.code === 200){
                    this.crowd = result.crowdSize - 3;
                }
            } catch (error) {
                console.log(error);
            }
        },

        async getWeather(){
            var wcURL = "http://127.0.0.1:7002/weatherCheck/forecast";
            // var wcURL = "https://themepark-5sdwlfnn.uc.gateway.dev/forecast";
            try {
                const response = await fetch(
                    wcURL,{
                        method: "GET",
                        // headers: {"Content-Type": "application/json"}
                    });
                const result = await response.json();
                if (result.code === 200){
                    this.forecast = result.forecast;
                    if (result.forecast.includes("Thunder")){
                        this.thunder = true;
                        this.rain = false;
                        this.cloud = false;
                        this.sun = false;
                    }
                    else if (result.forecast.includes("Shower")||result.forecast.includes("Rain")){
                        this.rain = true;
                        this.cloud = false,
                        this.sun = false;
                        this.thunder = false;
                    }
                    else if (result.forecast.includes("Cloud")){
                        this.cloud = true;
                        this.sun = false;
                        this.thunder = false;
                        this.rain = false;
                    }
                    else{
                        this.sun = true;
                        this.thunder = false;
                        this.rain = false;
                        this.cloud = false;
                    }
                }
            } catch (error) {
                console.log(error);
            }
        },

        navToDashboard(){
            this.$router.push('/dashboard'); 
        }
    },
    
    mounted(){
        if (this.store.uid != "XiV2CwmCzqUCFxJCjxuGpDPUzMY2" && this.store.uid != "48e6aimiq3VNF45VylXA6UAVODd2"){
            alert("You're not an admin");
            this.$router.push('/');
        }
        this.getTotalCrowd();
        setInterval(function(){ this.getTotalCrowd()}.bind(this), 1000);
        this.getWeather();
        setInterval(function(){ this.getWeather()}.bind(this), 180000);
    }
}
</script>
