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
                    <div class="col-md-3 text-lg-right my-auto">
                        <h4 v-show="joined&&available" class="card-title mb-0">Queue #: {{queueNumber}}</h4>
                    </div>
                    <div class="col-12">
                        <hr class="my-2">
                    </div>
                    <div class="col-0 col-md-5 text-lg-left" >
                        
                    </div>
                    <div class="col-0 col-md-1 my-auto">
                    </div>
                    <div class="col-6 col-md-3 my-auto">
                        <div v-if="available" class="card-text">
                            <h3 class="m-0"><strong>{{time}}</strong></h3>
                            <span> Wait Time (mins)</span>
                        </div>
                    </div>
                    <div class="col-6 col-md-2 my-auto">
                        <div v-if="available" class="card-text">
                            <h3 class="m-0"><strong>{{count}}</strong></h3>
                            <span v-if="!joined">In Queue</span>
                            <span v-else>Before You</span>
                        </div>
                    </div>
                    <div class="col-md-1 my-auto">
                        <button v-show="!joined&&available" type="button" class="btn btn-success float-lg-right" @click="joinqueue">Join Queue</button>
                        <button v-show="joined&&available" type="button" class="btn btn-danger float-lg-right" @click="leavequeue">Leave Queue</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
//import firebase from "firebase";

export default {
    data(){
        return{
            count: 0,
            attrName: this.attraction,
            joined: false,
            queueNumber: 0,
            available: true,
            badWeatherMessage: "",
            notified: false,
            time: 0
        }
    },
    
    inject: ["store"],

    props: {
        attraction: {
            type: String
        },
    },

    methods:{
        async joinqueue(){
            if (this.store.inQueue) {
                alert("You can only queue for one attraction at a time :(\n Leave your current queue to join a new one! :)");
            }
            var jqURL = "http://127.0.0.1:7000/joinQueue/join";
            // var jqURL = "https://themepark-5sdwlfnn.uc.gateway.dev/join";
            // var jqURL = "https://themepark-5sdwlfnn.uc.gateway.dev/join";
            try {
                const response = 
                await fetch(
                    jqURL, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "attractionName": this.attrName,
                        "customerID": this.store.uid, // eslint-disable-line no-undef
                        "name": this.store.username // eslint-disable-line no-undef
                    })
                    });
                const result = await response.json();
                if (result.code === 201){
                    this.queueNumber = result.queueNumber
                    this.joined = true;
                    this.store.inQueue = true;
                    console.log("Successfully joined queue");
                }
            } catch (error) {
                console.log(error);
            }
        },

        async leavequeue(){
            var lqURL = "http://127.0.0.1:8000/updateQueue/leave";
            // var lqURL = "https://themepark-5sdwlfnn.uc.gateway.dev/leave";
            // var lqURL = "https://themepark-5sdwlfnn.uc.gateway.dev/leave";
            try {
                const response = 
                await fetch(
                    lqURL, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "attractionName": this.attrName,
                        "customerID": this.store.uid, // eslint-disable-line no-undef
                    })
                    });
                const result = await response.json();
                if (result.code === 200){
                    this.joined = false;
                    this.store.inQueue = false;
                    this.notified = false;
                    console.log("Successfully left queue");
                }
            } catch (error) {
                console.log(error);
            }
        },

        async getQueue(){
            var qsURL = "http://127.0.0.1:7001/viewStatus/status/" + this.store.uid + "/" + this.attrName;
            // var qsURL = "https://themepark-5sdwlfnn.uc.gateway.dev/viewStatus/status/" + this.store.uid + "/" + this.attrName;
            try{
                const response = await fetch(
                    qsURL,{
                        method: "GET",
                        // headers: {"Content-Type": "application/json"},
                    });
                const result = await response.json();
                console.log(result);
                if (result.code === 200){
                    if(result.currentAttraction == ""){
                        this.joined = false;
                        this.store.inQueue = false;
                    }
                    else if (result.currentAttraction != this.attrName){
                        this.joined = false;
                        this.store.inQueue = true;
                    }
                    else{
                        this.joined = true;
                        this.store.inQueue = true;
                    }
                    this.count = result.numberInQueue;
                    this.time = result.waitTime;
                }
            } catch (error) {
                console.log(error);
            }
        },

        async getAvailabilty(){
            var wcURL = "http://127.0.0.1:7002/weatherCheck/availability/" + this.attrName;
            // var wcURL = "https://themepark-5sdwlfnn.uc.gateway.dev/availability/" + this.attrName;
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
        
        notification(){
            if (this.joined && this.count <= 3 && !this.notified){
                this.notified = true;
                alert(`Your turn is reaching soon, please make your way to the entrance of the ${this.attrName}.`);
            }
        }
    },
    mounted(){
        this.getQueue();
        setInterval(function(){ this.getQueue()}.bind(this), 1000);
        this.getAvailabilty();
        setInterval(function(){ this.getAvailability()}.bind(this), 1800000);
        this.notification();
        setInterval(function(){this.notification()}.bind(this), 1000)
    },
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
}
</script>
