import React = require("react");
import Chart from "react-apexcharts";
import { GenericStatistics } from "../../State";

type MethodChartProps = {
    data: GenericStatistics,
    chartHeight?: string,
    chartWidth?: string 
} & React.HTMLAttributes<HTMLDivElement>

type MethodChartState = {
    options: any,
    series: any,
  }

type ChartData = {
    categories: string[], 
    data: number[]
}

export class MethodsBarChart extends React.Component<MethodChartProps, MethodChartState> {
    constructor(props: MethodChartProps) {
        super(props);

        const statistics: ChartData = this.extract_methods_data()

        this.state = {
            options: {
                chart: {
                    id: "basic-bar"
                },
                xaxis: {
                    categories: statistics.categories
                },
                responsive: [{
                  breakpoint: 480,
                  options: {
                      chart: {
                          width: 300
                      },
                          legend: {
                          position: 'bottom'
                      }
                  }
              }],
                plotOptions: {
                    bar: {
                      horizontal: true,
                    }
                },
                dataLabels: {
                  enabled: false
                },
                title: {
                  text: "Channels Per Method",
                  align: "center"
                }

            },
            series: [
              {
                name: "Channel' Count",
                data: statistics.data
              }
            ]
          };
        
    }
    private extract_methods_data: any = (): ChartData => {
        const data: GenericStatistics = this.props.data;
        const categories: string[] = Object.keys(data).map(key => key);
        const series: number[] = Object.keys(data).map(key => data[key]);

        const formatted = {
            categories: categories,
            data: series

        }
        
        return formatted;
    };

  render() {    
    const height = this.props.chartHeight;
    const width = this.props.chartWidth;
    const className = `${this.props.className !== undefined ? this.props.className : ""}`;
    return (
      <div className={className}>
        <Chart
          options={this.state.options}
          series={this.state.series}
          type="bar"
          width={width}
        />
      </div>
    );
  }
}

