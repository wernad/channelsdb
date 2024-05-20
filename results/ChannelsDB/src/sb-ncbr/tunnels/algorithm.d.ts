/**
 * Copyright (c) 2024 mol* contributors, licensed under MIT, See LICENSE file for more info.
 *
 * @author Dušan Veľký <dvelky@mail.muni.cz>
 */
import { Mesh } from 'molstar/lib/mol-geo/geometry/mesh/mesh';
import { WebGLContext } from 'molstar/lib/mol-gl/webgl/context';
import { Shape } from 'molstar/lib/mol-model/shape';
import { Color } from 'molstar/lib/mol-util/color';
import { Tunnel } from './data-model';
export declare function createSpheresShape(options: {
    tunnel: Tunnel;
    color: Color;
    resolution: number;
    sampleRate: number;
    showRadii: boolean;
    prev?: Shape<Mesh>;
}): Promise<Shape<Mesh>>;
export declare function createTunnelShape(options: {
    tunnel: Tunnel;
    color: Color;
    resolution: number;
    sampleRate: number;
    webgl: WebGLContext | undefined;
    prev?: Shape<Mesh>;
}): Promise<Shape<Mesh>>;
