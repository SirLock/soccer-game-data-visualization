import {Coordinates} from "@/models/coordinates";
import {v4} from 'uuid';
import {Player} from "@/models/player";

export class Glyph {
    readonly id: string | undefined;
    coordinates: Coordinates | undefined;
    frame: number | undefined;
    width: number | undefined;
    height: number | undefined;
    svg: string | undefined;
    zIndex: number | undefined;
    labelText: string | undefined;
    representedObject: Player | Event | undefined;

    constructor(init: Partial<Glyph>) {
        this.id = v4();
        this.coordinates = init.coordinates;
        this.frame= init.frame;
        this.width = init.width;
        this.height = init.height;
        this.svg = init.svg;
        this.zIndex = init.zIndex;
        this.labelText = init.labelText;
        this.representedObject = init.representedObject;
    }

    get left(): number {
        // @ts-ignore
        return this.coordinates.x - this.width / 2;
    }

    get top(): number {
        // @ts-ignore
        return this.coordinates.y - this.height / 2;
    }
}