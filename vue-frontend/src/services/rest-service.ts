import {GameData} from "@/models/game-data";
import {FieldPart} from "@/models/field-part"

export class RestService {
    private static INSTANCE: RestService;

    public static getInstance(): RestService {
        if (!this.INSTANCE) {
            this.INSTANCE = new RestService();
        }
        return this.INSTANCE;
    }

    private constructor() {
    }

    private baseAddress = 'http://localhost:5000';

    async requestBasicInformation(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-basic-game-information/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestEvents(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-events-of/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestPlayers(dataSetId: string, team: string) {
        const params = `${dataSetId}$${team}`;
        const gResponse = await fetch(
            `${this.baseAddress}/get-players-of/${params}`
        );
        return await gResponse.json();
    }

    async requestTrackingData(dataSetId: string, team: string) {
        const params = `${dataSetId}$${team}`;
        const gResponse = await fetch(
            `${this.baseAddress}/get-tracking-data-of/${params}`
        );
        return await gResponse.json();
    }

    async requestBasicData(dataSetId: string): Promise<GameData> {
        const gResponse = await fetch(
            `${this.baseAddress}/get-basic-game-data/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestChallengesLeadingToShots(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-challenges-leading-to-shot/${dataSetId}`
        );
        return await gResponse.json();
    }

    
    async requestCounters(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-counters/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestGoals(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-goals/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestShots(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-shots/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestFaults(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-faults/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestCorners(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-corners/${dataSetId}`
        );
        return await gResponse.json();
    }


    async requestFreeKicks(dataSetId: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-free-kicks/${dataSetId}`
        );
        return await gResponse.json();
    }


    async requestAttackThroughLeftSide(dataSetId: string) {
        const gResponse = await fetch(
            `http://localhost:5000/get-attack-through-left-side/${dataSetId}`
        );
        return await gResponse.json();
    }

    async requestAttackThroughFieldPart(dataSetId: string, fieldPartName: string) {
        const gResponse = await fetch(
            `http://localhost:5000/get-attack-through-field-part/${dataSetId}/${fieldPartName}`
        );
        return await gResponse.json();
    }

    async requestPassesWithin(dataSetId: string, startFrame: number, endFrame: number) {
        const params = `${dataSetId}$${startFrame}$${endFrame}`;
        const gResponse = await fetch(
            `${this.baseAddress}/get-passes-within/${params}`
        );
        return await gResponse.json();
    }

    async requestEventsWithin(dataSetId: string, startFrame: number, endFrame: number) {
        const params = `${dataSetId}$${startFrame}$${endFrame}`;
        const gResponse = await fetch(
            `${this.baseAddress}/get-events-within/${params}`
        );
        return await gResponse.json();
    }

    async requestRelevantPlayersByDistance(dataSetID: string, teamID: string, startFrame: number, endFrame: number, relevantDistance: number) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-relevant-players-by-distance/${dataSetID}/${teamID}/${startFrame}/${endFrame}/${relevantDistance}`
        );
        return await gResponse.json();
    }

    async requestRelevantPlayersByPassParticipation(dataSetID: string, startFrame: number, endFrame: number) {
        const params = `${dataSetID}$${startFrame}$${endFrame}`;
        const gResponse = await fetch(
            `${this.baseAddress}/get-relevant-players-by-pass-participation/${params}`
        );
        return await gResponse.json();
    }
    
    async requestTraveledDistances(dataSetID: string) {
        const gResponse = await fetch(
            `${this.baseAddress}/get-traveled-distances/${dataSetID}`
        );
        return await gResponse.json(); 
    }

}