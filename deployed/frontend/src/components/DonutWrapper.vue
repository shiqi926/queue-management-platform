<template>
    <div class="container card my-5 p-4">
        <h4>Daily Breakdown</h4>
        <doughnut-chart
            v-if="loaded"
            :chartdata="chartdata"
            :options="options"/>
        <button class="btn btn-outline-info mt-5" @click="loadData">Refresh</button>        
        </div>
</template>

<script>
import DoughnutChart from './DonutCard.vue'

export default {
    name: 'DoughnutChartContainer',
    components: { DoughnutChart },
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
            // var adURL = "http://127.0.0.1:7003/dashboard/pie";
            var adURL = "https://themepark-5sdwlfnn.uc.gateway.dev/dashboard/pie?key=" + this.store.apiKey;
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