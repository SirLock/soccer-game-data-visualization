import { Coordinates } from "./coordinates";

export class Challenges {
    winner: string;
    loser: string;
    frame: number;
    time: number;
    subtype: string;
    fault: boolean;
    coordinates: Coordinates;
    
    public constructor(init:any) {
        this.winner = init?.winner;
        this.loser = init?.loser;
        this.frame = init?.frame;
        this.time = init?.time;
        this.subtype = init?.subtype;
        this.fault = init?.fault;
        this.coordinates = init?.coordinates;
    }
}