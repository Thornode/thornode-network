import React, { Component } from "react";
import { Chart } from "chart.js";

class CustomLineChart extends Component {
  chartRef = React.createRef();

  componentDidMount() {
    this.chartInstance = new Chart(this.chartRef.current, {
      type: "line",
      data: this.props.data,
      options: this.props.options,
    });
  }

  componentWillUnmount() {
    this.chartInstance.destroy();
  }

  render() {
    return <canvas ref={this.chartRef} />;
  }
}

export default CustomLineChart;
