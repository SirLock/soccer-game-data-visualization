import {Coordinates} from "@/models/coordinates";

export class Event {
    id: number
    team: string;
    type: string;
    subtype: string;
    period: number;
    startFrame: number;
    startTime: number;
    endFrame: number;
    endTime: number;
    origin: string;
    target: string;
    start: Coordinates;
    end: Coordinates;

    public constructor(init: any) {
        this.id = init?.id;
        this.team = init?.team;
        this.type = init?.type;
        this.subtype = init?.subtype;
        this.period = init?.period;
        this.startFrame = init?.startFrame;
        this.startTime = init?.startTime;
        this.endFrame = init?.endFrame;
        this.endTime = init?.endTime;
        this.origin = init?.origin;
        this.target = init?.target;
        this.start = init?.start;
        this.end = init?.end;
    }
}