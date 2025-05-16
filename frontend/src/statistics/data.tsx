import React = require("react");
import { GenericStatistics } from "../State";

type MethodChartProps = {
    title: string, 
    data: GenericStatistics
} & React.HTMLAttributes<HTMLDivElement>;

type MethodChartState = {
    avg: number,
    min: number, 
    max: number,
    median: number,
    deviation: number
  }

export class BasicDataSheet extends React.Component<MethodChartProps, MethodChartState> {
    constructor(props: MethodChartProps) {
        super(props);

        const data: GenericStatistics = this.props.data;

        this.state = {
            avg: data.avg,
            min: data.min,
            max: data.max,
            median: data.median,
            deviation: data.stdev,
        };
        
    }


  render() {    
    const className = `${this.props.className !== undefined ? this.props.className : ""}`;

    return (
        <div className={`p-3 border border-primary row ${className}`}>
            <p className="mb-1 h2">{this.props.title}</p>
            <div className="col-xs-6">
                <p>Minimum: {this.state.min}</p>
                <p>Maximum: {this.state.max}</p>
            </div>
            <div className="col-xs-6">
                <p>Median: {this.state.median}</p>
                <p>Average: {this.state.avg}</p>
                <p>Deviation: {this.state.deviation}</p>
            </div>
        </div>
    );
  }
}

