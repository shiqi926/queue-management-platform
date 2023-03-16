<template>
    <div class="about bg">
        <div class="jumbotron jumbotron-fluid mb-3 bg-light">
            <div class="container">
                <h2 class="display-4">Good morning {{store.username}}</h2>
                <p class="lead">Welcome to the Dashboard. Here is an overview of the rides today.
    
                </p>
            </div>
        </div>
        <div class="container">
            <DonutWrapper></DonutWrapper>
            <div v-for="attr in attractionsList" :key="attr">
                <DashboardWrapper v-bind:attraction="attr"></DashboardWrapper>
            </div>
        </div>
    </div>
</template>

<style>
    .bg {
        background: lightblue;
        width: 100vw;
        height: 350vh;
    }
</style>

<script>
import DashboardWrapper from "@/components/DashboardWrapper.vue"
import DonutWrapper from "@/components/DonutWrapper.vue"

export default {
    name: 'Dashboard',
    data(){
        return{
            attractionsList: ["Viking Ship", "Rollercoaster", "Carousell"],
            crowd: 0     
        }
    },
    
    inject: ["store"],

    components:{
        DashboardWrapper,
        DonutWrapper
    },
    
    mounted(){
        if (this.store.uid != "XiV2CwmCzqUCFxJCjxuGpDPUzMY2" && this.store.uid != "48e6aimiq3VNF45VylXA6UAVODd2"){
            alert("You're not an admin");
            this.$router.push('/');
        }
        // this.getTotalCrowd();
        // setInterval(function(){ this.getTotalCrowd()}.bind(this), 5000);
    }
}


</script>