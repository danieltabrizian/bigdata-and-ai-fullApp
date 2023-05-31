

<template>
  <canvas  style="width: 800px;height: 500px" ref="chart"></canvas>
  <HelloWorld msg="sfddsf"/>
</template>

<script>

import HelloWorld from "@/components/HelloWorld.vue";
import Chart from 'chart.js/auto';

export default {
  components: {HelloWorld},
  data(){
    return{
      data: [
    { year: 2010, count: 10 },
    { year: 2011, count: 20 },
    { year: 2012, count: 15 },
    { year: 2013, count: 25 },
    { year: 2014, count: 22 },
    { year: 2015, count: 30 },
    { year: 2016, count: 28 },
  ]
    }
  },
  mounted() {
    this.setup();
  },
  methods:{
    setup(){
      new Chart(
        this.$refs.chart,
        {
          type: 'line',
          options:{
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Month'
                }
              },
              y: {
                stacked: true,
                title: {
                  display: true,
                  text: 'Value'
                }
              }
            },
          },
          data: {
            labels: this.data.map(row => row.year),
            datasets: [
              {
                label: 'Acquisitions by year',
                data: this.data.map(row => row.count),
                fill: true,
                stacked: true
              },
                {
                label: 'Acquisitions by year',
                data: this.data.map(row => row.count),
                fill: true,
                  stacked: true
              }
            ]
          }
        }
      );
    }
  }
}
</script>

<style scoped>

</style>
