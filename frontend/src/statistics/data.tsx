import React = require("react");
import { ExtendedStatistics } from "../State";

type MethodChartProps = {
    title: string,
    data: ExtendedStatistics
} & React.HTMLAttributes<HTMLDivElement>;

type MethodChartState = {
    avg: number,
    min: number,
    max: number,
    median: number,
    deviation: number
    minStructure: string,
    maxStructure: string,
}

export class BasicDataSheet extends React.Component<MethodChartProps, MethodChartState> {
    constructor(props: MethodChartProps) {
        super(props);

        const data: ExtendedStatistics = this.props.data;

        this.state = {
            avg: data.avg as number,
            min: data.min as number,
            max: data.max as number,
            median: data.median as number,
            deviation: data.stdev as number,
            minStructure: data.min_structure_id as string,
            maxStructure: data.max_structure_id as string,
        };

    }


    render() {
        const className = `${this.props.className !== undefined ? this.props.className : ""}`;
        const minStructure = this.state.minStructure;
        const maxStructure = this.state.maxStructure;

        return (
            <div className={`p-4 border rounded shadow-sm bg-light mb-3 ${className}`}>
                <p className="h4 fw-semibold text-primary mb-3">{this.props.title}</p>
                <div className="row">
                    <div className="col-md-6 mb-2">
                        <p className="mb-1"><strong>Minimum:</strong> {this.state.min} {minStructure !== undefined && <a href={`/detail?pid=${minStructure}`}>({minStructure})</a>}</p>
                        <p className="mb-1"><strong>Maximum:</strong> {this.state.max} {maxStructure !== undefined && <a href={`/detail?pid=${maxStructure}`}>({maxStructure})</a>}</p>
                    </div>
                    <div className="col-md-6 mb-2">
                        <p className="mb-1"><strong>Median:</strong> {this.state.median}</p>
                        <p className="mb-1"><strong>Average:</strong> {this.state.avg}</p>
                        <p className="mb-1"><strong>Deviation:</strong> {this.state.deviation}</p>
                    </div>
                </div>
            </div >
        );
    }
}

