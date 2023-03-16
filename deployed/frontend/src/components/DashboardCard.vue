<script>
//import {Chart, LineController, Line, Point, LinearScale, Title} from 'chart.js'
import { Line } from 'vue-chartjs'
//Chart.register(LineController, Line, Point, LinearScale, Title)
//import { Line, mixins } from 'vue-chartjs'
//const { reactiveProp } = mixins

export default {
    extends: Line,
    //mixins: [reactiveProp],

    props: {
        chartdata: {
            type: Object,
            default: null
        },
        options: {
            type: Object,
            default: null
        }
    },

    mounted () {
        this.renderChart(this.chartdata, this.options);
    }

}

</script>