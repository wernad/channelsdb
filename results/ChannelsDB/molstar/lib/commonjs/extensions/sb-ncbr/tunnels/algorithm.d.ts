import { Mesh } from "../../../mol-geo/geometry/mesh/mesh";
import { WebGLContext } from "../../../mol-gl/webgl/context";
import { Shape } from "../../../mol-model/shape";
import { Color } from "../../../mol-util/color";
import { Tunnel } from "./props";
export declare function createSpheresShape(tunnel: Tunnel, color: Color, resolution: number, webgl?: WebGLContext): Promise<Shape<Mesh>>;
export declare function createTunnelShape(tunnel: Tunnel, color: Color, resolution: number, webgl?: WebGLContext): Promise<Shape<Mesh>>;
