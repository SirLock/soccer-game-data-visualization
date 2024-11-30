import {Coordinates} from "./coordinates";

export class FrameElement {
    period: number;
    frame: number;
    time: number;
    coordinates: Map<string, Coordinates>;

    public constructor(init: FrameElement) {
        this.period = init.period;
        this.frame = init.frame;
        this.time = init.time;
        this.coordinates = init.coordinates;
    }
}