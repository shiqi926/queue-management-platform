<template>
    <div class="card bg-light mb-3" style="border-radius: 1.5rem;">
        <!-- <img class="card-img-top" height='230px' width ='350px' :src="image" alt="Card image cap"> -->
        <div class="card-body">
            <div class="container">
                <div class="row">
                    <div class="col-md-3 text-lg-left my-auto">
                        <h3 class="card-title mb-0" style="display:inline;">{{attrName}}</h3>
                    </div>
                    <div class="col-md-6 text-lg-left my-auto">
                        <h5 v-if="!available" class="card-title mb-0">{{badWeatherMessage}}
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cloud-lightning-rain" viewBox="0 0 16 16">
                                <path d="M2.658 11.026a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm9.5 0a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm-7.5 1.5a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm9.5 0a.5.5 0 0 1 .316.632l-.5 1.5a.5.5 0 1 1-.948-.316l.5-1.5a.5.5 0 0 1 .632-.316zm-.753-8.499a5.001 5.001 0 0 0-9.499-1.004A3.5 3.5 0 1 0 3.5 10H13a3 3 0 0 0 .405-5.973zM8.5 1a4 4 0 0 1 3.976 3.555.5.5 0 0 0 .5.445H13a2 2 0 0 1 0 4H3.5a2.5 2.5 0 1 1 .605-4.926.5.5 0 0 0 .596-.329A4.002 4.002 0 0 1 8.5 1zM7.053 11.276A.5.5 0 0 1 7.5 11h1a.5.5 0 0 1 .474.658l-.28.842H9.5a.5.5 0 0 1 .39.812l-2 2.5a.5.5 0 0 1-.875-.433L7.36 14H6.5a.5.5 0 0 1-.447-.724l1-2z"/>
                            </svg>
                        </h5>
                    </div>
                </div>
                <div v-if="available" class = "row">
                    <!-- Summary Section -->
                    <div class="col-12">
                        <hr class="my-2">
                    </div>
                    <div class="col-4 my-auto">
                        <div class="card-text">
                            <h4 class="m-0"><strong>{{time}}</strong></h4>
                            <span>Waiting Time (mins)</span>
                        </div>
                    </div>
                    <div class="col-4 my-auto">
                        <div class="card-text">
                            <h4 class="m-0"><strong>{{count}}</strong></h4>
                            <span>In Queue</span>
                        </div>
                    </div>
                    <div class="col-4 my-auto">
                        <div class="card-text" id="countdown">
                            <h4 class="m-0"><strong><span>{{minutes}}</span>:<span>00</span></strong></h4> 
                            <span>Ride Timer</span>
                        </div>
                    </div>
                <div class="col-12">
                    <hr class="my-2">
                </div>
                </div>
                <div class ="row mt-2 px-2">
                    <!-- Customers Section -->
                    <div class="btn-grp">
                            <!-- This is the repeated part -->
                            <button class="btn btn-secondary mx-1" v-for="cust in custList" :key="cust">
                                <input type="checkbox" :id="cust.customerID" :value="cust.customerID" v-model="checkedList">
                                {{cust.name}}
                                <br>
                                #{{cust.queueNumber}}
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                                    <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                                    <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
                                </svg>
                            </button>
                    </div>
                </div>
                <div v-if="available" class ="row">
                    <div class="col-12">
                        <hr class="my-2">
                    </div>
                    <div class="col-6 my-auto">
                        <button type="button" class="btn btn-success" @click="start">
                            Start Ride
                        </button>
                    </div>
                    <div class="col-6 my-auto">
                        <button type="button" class="btn btn-danger" @click="remove('REMOVED')">Remove from Queue</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    #countdown li {
        display: inline-block;
    }
    #countdown li span {
        display: block;
    }
</style>

<script>
//import firebase from "firebase";
export default {
    data(){
        return{
            count: 0,
            attrName: this.attraction,
            available: true,
            badWeatherMessage: "",
            custList: [],
            checkedList: [],
            time: 0,
            minutes: 0,
            duration: 0
        }
    },
    
    inject: ["store"],

    props: {
        attraction: {
            type: String
        },
    },

    methods:{
        
        async getCustomers(){
            // var gcURL = "http://127.0.0.1:5001/attractions/attractionSorted/" + this.attrName;
            var gcURL = "https://themepark-5sdwlfnn.uc.gateway.dev/attractionSorted/" + this.attrName + "?key=" + this.store.apiKey;
            try {
                const response = await fetch(
                    gcURL,{
                        method: "GET",
                        // headers: {"Content-Type": "application/json"},
                    });
                const result = await response.json();
                if (result){
                    this.custList = result;
                }
            } catch (error) {
                console.log(error);
            }
        },
        async getQueue(){
            if (this.available){
                // var gqURL = "http://127.0.0.1:7001/viewStatus/" + this.attrName;
                var gqURL = "https://themepark-5sdwlfnn.uc.gateway.dev/viewStatus/" + this.attrName + "?key=" + this.store.apiKey;
                try {
                    const response = await fetch(
                        gqURL,{
                            method: "GET",
                            // headers: {"Content-Type": "application/json"},
                        });
                    const result = await response.json();
                    if (result.code === 200){
                        this.count = result.numberInQueue;
                        this.time = result.waitTime;
                    }
                } catch (error) {
                    console.log(error);
                }
            }
        },

        async getAvailabilty(){
            // var wcURL = "http://127.0.0.1:7002/weatherCheck/availability/" + this.attrName;
            var wcURL = "https://themepark-5sdwlfnn.uc.gateway.dev/availability/" + this.attrName;
            try {
                const response = await fetch(
                    wcURL,{
                        method: "GET",
                        // headers: {"Content-Type": "application/json"}
                    });
                const result = await response.json();
                if (result.code === 200){
                    if (!result.available){
                        this.available = false;
                        this.badWeatherMessage = result.message
                    }
                }
            } catch (error) {
                console.log(error);
            }
        },
        
        async remove(action){
            // var rmURL = "http://127.0.0.1:8000/updateQueue/remove";
            // var rmURL = "https://themepark-5sdwlfnn.uc.gateway.dev/remove?key=" + this.store.apiKey;
            var rmURL = "https://themepark-5sdwlfnn.uc.gateway.dev/remove?key=" + this.store.apiKey;
            try {
                const response = await fetch(
                    rmURL, {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            "attractionName": this.attrName,
                            "removeList": this.checkedList,
                            "action": action
                        })
                    }
                );
                const result = await response.json();
                if (result.code === 200){
                    console.log("Removed");
                }
            } catch (error) {
                console.log(error);
            }
        },

        async getDetails(){
            // var adURL = "http://127.0.0.1:5002/attractionDetails/" + this.attrName;
            var adURL = "https://themepark-5sdwlfnn.uc.gateway.dev/attractionDetails/" + this.attrName + "?key=" + this.store.apiKey;
            try{
                const response = await fetch(
                    adURL, {
                        method: "GET",
                        // headers: {"Content-Type": "application/json"},
                    }
                );
                const result = await response.json();
                if (result.code === 200) {
                    this.duration = result.attDet.duration;
                }
            } catch (error) {
                console.log(error);
            }
        },

        start: function(){
            this.minutes = this.duration;
            this.countDownTimer();
        },

        countDownTimer(){
            if(this.minutes > 0) {
                setTimeout(() => {
                    this.minutes -= 1
                    this.countDownTimer()
                }, 1000)
            }
            else {
                this.remove("BOARDED");
            }
        }
    },
    
    mounted(){
        this.getDetails();
        this.getCustomers();
        setInterval(function(){ this.getCustomers()}.bind(this), 1000);
        this.getQueue();
        setInterval(function(){ this.getQueue()}.bind(this), 1000);
        this.getAvailabilty();
        setInterval(function(){ this.getAvailability()}.bind(this), 1800000);
    }
//   created() {
//     // eslint-disable-next-line no-unused-vars
//     const observer = firebase.firestore().collection('attractions').where('attractionName', '==', this.attraction)
//         .onSnapshot(querySnapshot => {
//             querySnapshot.docChanges().forEach(change => {
//             if (change.type === 'added') {
//                 this.count++;
//             }
//             if (change.type === 'modified') {
//                 this.count--;
//             }
//             if (change.type === 'removed') {
//                 this.count--;
//             }
//             });
//   });      

//   }
};

</script>