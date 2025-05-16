import React from "react";
import { StatisticsData } from "../State"
import { MethodsBarChart } from "./charts/bar";
import { PieChart } from "./charts/pie";
import { BasicDataSheet } from "./data";

type StatisticsProps = {
    "statistics": StatisticsData
}

export class Statistics extends React.Component<StatisticsProps, {}> {

    render() {
        const { statistics } = this.props;
        const total = Object.keys(statistics.methods ?? {}).reduce((acc, key) => acc + statistics.methods[key], 0)

        return (
            <div className="container">
                {total > 0 ?
                    <div className="row">
                        <div className="col-md-4 d-flex flex-column gap-3">
                            <PieChart pieSize={0.5} className="mb-3" subtractTotal={true} title="Top 5 Channel Types" data={statistics.top_types} />
                            <PieChart pieSize={0.5} className="mb-3" subtractTotal={true} title="Top 5 Proteins" data={statistics.top_proteins} />
                            <PieChart pieSize={0.5} className="mb-3" subtractTotal={false} title="Top 5 Residues" data={statistics.top_residues} />
                        </div>
                        <div className="col-md-4">
                            <MethodsBarChart chartWidth="500px" data={statistics.methods} />
                            <BasicDataSheet className="mb-3" title="Channel Length" data={statistics.length} />
                            <BasicDataSheet className="mb-3" title="Bottleneck" data={statistics.bottleneck} />
                        </div>
                    </div>
                    : "No channels found..."}
            </div>
        );
    }
}