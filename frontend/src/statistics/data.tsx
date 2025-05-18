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
            <div className={`p-4 border rounded shadow-sm bg-light mb-3 ${className}`}>
                <p className="h4 fw-semibold text-primary mb-3">{this.props.title}</p>
                <div className="row">
                    <div className="col-md-6 mb-2">
                        <p className="mb-1"><strong>Minimum:</strong> {this.state.min}</p>
                        <p className="mb-1"><strong>Maximum:</strong> {this.state.max}</p>
                    </div>
                    <div className="col-md-6 mb-2">
                        <p className="mb-1"><strong>Median:</strong> {this.state.median}</p>
                        <p className="mb-1"><strong>Average:</strong> {this.state.avg}</p>
                        <p className="mb-1"><strong>Deviation:</strong> {this.state.deviation}</p>
                    </div>
                </div>
            </div>
        );
    }
}

