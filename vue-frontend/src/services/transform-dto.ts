import {FrameElement} from "@/models/frame-element";
import {Coordinates} from "@/models/coordinates";
import {Player} from "@/models/player";
import {BasicGameInformation} from "@/models/basic-game-information";
import {Situation} from "@/models/situation";

export class TransformDto {

    public static toMap<Type>(object: any): Map<string, Type> {
        const objectsMap = new Map<string, Type>();
        const keys = Object.keys(object);
        keys.forEach(key => objectsMap.set(key, object[key]));
        return objectsMap;
    }

    public static toCoordinatesMap(coordinates: any): Map<string, Coordinates> {
        return TransformDto.toMap<Coordinates>(coordinates);
    }

    public static toPlayersMap(players: any): Map<string, Player> {
        return TransformDto.toMap<Player>(players);
    }

    public static toSituations(situationsDtos: any[]): Situation[] {
        const situations: Situation[] = [];
        for (let situationDto of situationsDtos) {
            situations.push(Situation.fromSituationDto(situationDto));
        }
        return situations;
    }

    public static toBasicInformation(basicInformation: any): BasicGameInformation {
        const firstPeriodEnd = basicInformation.firstPeriodEnd;
        const secondPeriodStart = basicInformation.secondPeriodStart;
        return new BasicGameInformation({firstPeriodEnd, secondPeriodStart});
    }

    public static toTraveledDistancesMaps(traveledDistances: any): Map<string, any[]> {
        return TransformDto.toMap<Number[]>(traveledDistances);
    }


    public static toFrameElements(trackingData: any): FrameElement[] {
        const frameElements: FrameElement[] = [];
        for (let row of trackingData) {
            const coordinates = this.toCoordinatesMap(row.coordinates);
            frameElements.push(new FrameElement({
                period: row.period,
                frame: row.frame,
                time: row.time,
                coordinates: coordinates
            }));
        }
        return frameElements;
    }
}