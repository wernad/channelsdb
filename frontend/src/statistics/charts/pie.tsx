import React = require("react");
import Chart from "react-apexcharts";
import { GenericStatistics } from "../../State";

type GenericWithTotal = GenericStatistics | { total: number };

type PieChartProps = {
    title: string,
    data: GenericWithTotal,
    subtractTotal: boolean
    pieSize: number,
} & React.HTMLAttributes<HTMLDivElement>;

type PieChartState = {
    options: any,
    series: any,
}

type ChartData = {
    labels: string[],
    data: number[]
}

const COLORS: string[] = [
    '#4e79a7',  // Blue
    '#f28e2c',  // Orange
    '#e15759',  // Red
    '#76b7b2',  // Teal
    '#59a14f',  // Green
    '#edc949',  // Yellow
    '#af7aa1',  // Purple
    '#ff9da7',  // Pink
    '#9c755f',  // Brown
    '#bab0ab'   // Gray
];

export class PieChart extends React.Component<PieChartProps, PieChartState> {
    constructor(props: PieChartProps) {
        super(props);

        const statistics: ChartData = this.extract_pie_data()

        this.state = {
            options: {
                labels: statistics.labels,
                title: {
                    text: this.props.title,
                    align: "center"
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
                    pie: {
                        donut: {
                            labels: {
                                show: true,
                                name: {
                                    show: true
                                },
                                value: {
                                    show: true
                                }
                            },
                            customScale: this.props.pieSize
                        }
                    }
                },
                colors: COLORS
            },
            series: statistics.data
        };

    }

    private extract_pie_data: any = (): ChartData => {
        const data: GenericStatistics = this.props.data;
        const top_sum = Object.keys(data)
            .filter(k => k !== 'total')
            .reduce((acc, k) => acc + data[k], 0);

        const labels: string[] = Object.keys(data).map(key => {
            if (key === 'total') {
                return "The rest"
            }
            return key;
        });
        const series: number[] = Object.keys(data).map(key => {
            if (key === 'total' && this.props.subtractTotal === true) {
                return data[key] - top_sum;
            }
            return data[key];
        });

        const formatted = {
            labels: labels,
            data: series

        }

        return formatted;
    };

    render() {
        const className = `${this.props.className !== undefined ? this.props.className : ""}`;

        return (
            <div className={className}>
                <Chart
                    options={this.state.options}
                    series={this.state.series}
                    type="donut"
                />
            </div>
        );
    }
}

