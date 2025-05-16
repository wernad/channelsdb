import React from "react";
import { GlobalRouter } from "../SimpleRouter";
import { IDType } from "../DataInterface";

export class PdbIdSign extends React.Component<{}, {}> {

    componentDidMount() {
    }

    componentWillUnmount() {
    }

    render() {
        let pid = GlobalRouter.getCurrentPid();
        let idType = GlobalRouter.getCurrentPidType();
        let oldPid = GlobalRouter.tryGetOldPdbId();

        return <>
            <div id="pdbid-sign" className="current-pdbid-sign">
                <a href={idType === IDType.PdbOld || idType === IDType.PdbNew ? `https://pdbe.org/${oldPid}` : `https://alphafill.eu/model?id=${pid}`} style={idType === IDType.PdbOld || idType === IDType.PdbNew ? {} : { fontSize: "14px" }} target="_blank">
                    {pid}
                    <span className="glyphicon glyphicon-new-window href-ico" />
                </a>
            </div>
        </>
    }
}

export default PdbIdSign;