<template>
  <div class="container">
    <ImageViewer msg="sfddsf"/>
    <canvas style="width: 800px;height: 500px" ref="chart"></canvas>
  </div>


</template>
<style scoped>
  .container{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
<script>

import ImageViewer from "@/components/ImageViewer.vue";
import Chart from 'chart.js/auto';

export default {
  components: {ImageViewer},
  data(){
    return{
      data: {
        "1": {"title": "Image 22-10-25 11-24-52_scaled", "ice cube": 2, "submarine": 1, "vertical": 2},
        "2": {"title": "Image 22-10-25 11-28-21_scaled", "vertical": 5, "ice cube": 2},
        "3": {"title": "Image 22-10-25 11-09-12_scaled", "ice cube": 2, "duplicate": 1, "submarine": 7}
      }
    }
  },
  mounted() {
    this.setup();
  },
  methods:{
    setup(){
      const labels = Object.keys(this.data);
      const datasets = this.createDatasets();

      new Chart(this.$refs.chart, {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              stacked: true,
              title: {
                display: true,
                text: 'Value'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Index'
              }
            }
          },
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Chart.js Bar Chart - Stacked'
            }
          }
        }
      });
    },
    createDatasets() {
      const uniqueKeys = ['duplicate','vertical','ice cube', 'submarine'];
      return uniqueKeys.map(key => {
        return {
          label: key,
          data: Object.values(this.data).map(item => item[key] || 0),
          stack: 'Stack 0',
          fill: 'origin'
        };
      });
    }
  }
}
</script>


