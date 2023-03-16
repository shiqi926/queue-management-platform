<template>
    <div class="container card my-5 p-4">
        <h4>{{attraction}}</h4>
        <line-chart
            v-if="loaded"
            :chartdata="chartdata"
            :options="options"/>
        <button class="btn btn-outline-info mt-5" @click="loadData">Refresh</button>
    </div>    
</template>

<script>
import LineChart from './DashboardCard.vue'

export default {
    name: 'LineChartContainer',
    components: { LineChart },
    props: {
        attraction: {
            type: String
        },
    },
    data: () => ({
        loaded: false,
        chartdata: null,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    }),
    inject: ["store"],
    methods:{
        async loadData(){
            this.loaded = false;
            // var adURL = "http://127.0.0.1:7003/dashboard/" + this.attraction;
            var adURL = "https://themepark-5sdwlfnn.uc.gateway.dev/dashboard/" + this.attraction + "?key=" + this.store.apiKey;
            try {
                const response = await fetch(
                        adURL, {
                            method: "GET",
                            // headers: {"Content-Type": "application/json"},
                        }
                    );
                const result = await response.json();
                if (result.code === 200){
                    this.chartdata = result.chartData;
                    this.loaded = true;
                }
            } catch (error) {
                console.error(error)
            }
        }
    },
    async mounted () {
        this.loadData();
    }
}
</script>