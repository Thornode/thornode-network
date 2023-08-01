import React, { Component } from "react";
import { Chart } from "chart.js";

class CustomLineChart extends Component {
  chartRef = React.createRef();
  chartInstance = null;
  componentDidMount() {
    this.createChart();
  }
  componentDidUpdate() {
    this.updateChart();
  }
  componentWillUnmount() {
    this.destroyChart();
  }
  createChart() {
    const { data, options } = this.props;
    this.chartInstance = new Chart(this.chartRef.current, {
      type: "line",
      data,
      options,
    });
  }
  updateChart() {
    const { data, options } = this.props;
    if (this.chartInstance) {
      this.chartInstance.data = data;
      this.chartInstance.options = options;
      this.chartInstance.update();
    }
  }
  destroyChart() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }
  }
  render() {
    return <canvas ref={this.chartRef} />;
  }
}

export default CustomLineChart;
