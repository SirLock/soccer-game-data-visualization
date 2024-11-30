import {FrameElement} from "@/models/frame-element";
import {Events} from "@/models/events";
import {Player} from "@/models/player";
import {BasicGameInformation} from "@/models/basic-game-information";

export class GameData {
    id: string;
    basicInformation: BasicGameInformation;
    trackingAway: FrameElement[];
    trackingHome: FrameElement[];
    playersAway: Map<string, Player>;
    playersHome: Map<string, Player>;
    traveledDistancesAway: Map<string, []>;
    traveledDistancesHome: Map<string, []>;
    events: Events;
    asJson: string;

    constructor(init: any) {
        this.id = init?.id;
        this.basicInformation = init?.basicInformation;
        this.trackingAway = init?.trackingAway;
        this.trackingHome = init?.trackingHome;
        this.playersAway = init?.playersAway;
        this.playersHome = init?.playersHome;
        this.traveledDistancesAway = init?.traveledDistancesAway;
        this.traveledDistancesHome = init?.traveledDistancesHome;
        this.events = init?.events;
        this.asJson = init?.asJson;
    }
}