import { IDType } from "./DataInterface";

export class URL {
    private url: string;
    private parts: string[];
    private hasHost: boolean;
    private parameters: Map<string, string>;
    private protocol: string;

    constructor(url: string, hasHost: boolean = true) {
        this.url = this.removeLastSlash(url);
        this.parts = this.removeTrailingSlashes(url).split("/");
        this.hasHost = hasHost;
        this.parameters = this.parseURLParameters(url);
        this.protocol = this.parseProtocol(url);
    }

    private removeProtocolPart(url: string) {
        let parts = this.url.split("//");
        return parts[parts.length - 1];
    }

    private removeLastSlash(url: string) {
        if (url[url.length - 1] === "/" || url[url.length - 1] === "\\") {
            return url.slice(0, url.length - 1);
        }

        return url;
    }

    private removeBeginingSlash(url: string) {
        if (url[0] === "/" || url[0] === "\\") {
            return url.slice(1);
        }

        return url;
    }

    private removeTrailingSlashes(url: string) {
        return this.removeLastSlash(this.removeBeginingSlash(this.removeProtocolPart(url)));
    }

    substractPathFromStart(path: string) {
        let substractPathParts = this.removeBeginingSlash(path).split("/");

        let urlSubstracted = [];
        for (let idx = (this.hasHost ? 1 : 0), i = 0; idx < this.parts.length; idx++, i++) {

            if (i < substractPathParts.length && this.parts[idx] === substractPathParts[i]) {
                continue;
            }

            urlSubstracted.push(this.parts[idx]);
        }
        console.log("subtract", urlSubstracted);
        return new URL(URL.constructPath(urlSubstracted), false);
    }

    getHostname() {
        if (!this.hasHost) {
            return "";
        }
        return this.parts[0];
    }

    getPart(index: number) {
        return this.parts[index];
    }

    getLength() {
        console.log("length", this.parts);
        return this.parts.length;
    }

    public static constructPath(pathParts: string[], useProtocol: boolean = false, protocol: string = "http"): string {
        let url = "";
        for (let i = 0; i < pathParts.length; i++) {
            if (pathParts[i] === "") {
                continue;
            }
            url += `/${pathParts[i]}`;
        }
        if (useProtocol) {
            url = `${protocol}:/${url}`;
        }
        return url;
    }

    getLastPart() {
        return this.getPart(this.getLength() - 1);
    }

    getParameterValue(name: string) {
        if (!this.parameters.has(name)) {
            return null;
        }

        let value = this.parameters.get(name);
        if (value === void 0) {
            return null;
        }

        return value;
    }

    private parseURLParameters(url: string) {
        let parts = url.split("?");

        let parameters = new Map<string, string>();

        if (parts.length !== 2) {
            return parameters;
        }

        let params = parts[1].split("&");
        for (let i = 0; i < params.length; i++) {
            let tuple = params[i].split("=");
            let key = tuple[0];
            let value = "";
            if (tuple.length === 2) {
                value = tuple[1];
            }
            parameters.set(key, value);
        }

        return parameters;
    }

    private parseProtocol(url: string) {
        let protocol = url.split(":");
        if (protocol.length > 1) {
            return protocol[0];
        }

        return "";
    }

    getProtocol() {
        if (!this.hasHost) {
            return "";
        }

        return this.protocol;
    }

    toString(): string {
        return URL.constructPath(this.parts, this.hasHost, this.getProtocol());
    }
}

export class Router {
    private contextPath: string;

    constructor(contextPath: string) {
        this.contextPath = contextPath;
    }

    /* Buggy !!
    getRelativePath(){
        return new SrURL(document.URL).substractPathFromStart(this.contextPath);
    }
    */

    getAbsoluePath() {
        return new URL(document.URL);
    }

    changeUrl(name: string, windowTitle: string, url: string) {
        let stateObj = { page: name };
        history.pushState(stateObj, windowTitle, url);
    }

}

export interface RoutingParameters {
    defaultContextPath: string,
    defaultPid: string,
};


export class GlobalRouter {
    private static defaultContextPath: string;
    private static defaultPid: string;
    private static currentPid: string;

    private static router: Router;

    private static defaultChannelsURL = "/api/v1";

    private static isInitialized: boolean = false;

    public static init(routingParameters: RoutingParameters) {
        console.log("panda1")
        if (!this.isInitialized) {
            console.log("panda2")
            this.defaultContextPath = routingParameters.defaultContextPath;
            this.defaultPid = routingParameters.defaultPid;

            this.router = new Router(routingParameters.defaultContextPath);

            let url = this.router.getAbsoluePath();

            let pid = url.getParameterValue("pid");
            if (pid === null) {
                let lastPathPartAsParam = url.substractPathFromStart(this.defaultContextPath).getLastPart();
                pid = lastPathPartAsParam === "" ? null : lastPathPartAsParam;
                console.log("null", pid);
            }


            if (pid === null) {
                this.currentPid = this.defaultPid;
                this.router.changeUrl("detail", document.title, `${url}/${this.currentPid}`);
                console.log("default", `${url}/${this.currentPid}`)
            } else {
                this.currentPid = pid;
            }
            this.isInitialized = true;
        } else {
            console.log("GlobalRouter is already initialized.");
        }
    }

    public static getCurrentPid() {
        if (!this.isInitialized) {
            throw new Error("GlobalRouter is not inititalised! Call init(..) function before use!");
        }

        return this.currentPid;
    }

    public static getCurrentPidType() {
        if (!this.isInitialized) {
            throw new Error("GlobalRouter is not inititalised! Call init(..) function before use!");
        }

        const oldPdbIdRegex = RegExp('^[1-9][a-z0-9]{3}$');
        // const newPdbIdRegex = RegExp('^pdb_[0-9]{5}[a-z0-9]{3}$'); # Might be used but for now not necessary.
        const alphafillRegex = RegExp('^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}');

        if (oldPdbIdRegex.test(this.currentPid) /*|| newPdbIdRegex.test(this.currentPid)*/) {
            return IDType.Pdb;
        }
        else if (alphafillRegex.test(this.currentPid)) {
            return IDType.Alphafill;
        }
        else {
            throw new Error("Unsupported ID format.");
        }
    }

    public static getChannelsURL() {
        if (!this.isInitialized) {
            throw new Error("GlobalRouter is not inititalised! Call init(..) function before use!");
        }

        return this.defaultChannelsURL;
    }

}