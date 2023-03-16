<template>
    <div class="about bg">
        <div class="jumbotron jumbotron-fluid mb-3 bg-light">
            <div class="container">
                <h1 class="display-4">Hello, {{store.username}}!</h1>
                <p class="lead">Welcome to the Themepark!</p>
            </div>
        </div>
        
        <div class="container">
            <div v-for="attr in attractionsList" :key="attr">
                <AttractionCard v-bind:attraction="attr"></AttractionCard>
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
import AttractionCard from "@/components/AttractionCard.vue"

export default {
    name: 'Gallery',
    data(){
        return{
            //userEmail: "",
            attractionsList: ["Viking Ship", "Rollercoaster", "Carousell"],
            userUID: ""     
        }
    },
    inject: ['store'],
    components:{
        AttractionCard
    }
}
</script>
