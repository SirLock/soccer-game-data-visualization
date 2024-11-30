import {v4} from "uuid";


export const CHALLENGE_LEADING_TO_SHOT = 'challenge_leading_to_shot';
export const ATTACKS_THROUGH_FIELD_PART = 'attacks_through_field_part';
export const ATTACKS_THROUGH_TOP = 'attacks_through_top';
export const ATTACKS_THROUGH_CENTER = 'attacks_through_center';
export const ATTACKS_THROUGH_BOTTOM = 'attacks_through_bottom';
export const COUNTERS = 'counters';
export const GOAL = 'goal';
export const CORNER = 'corner';
export const FREE_KICK = 'free_kick';
export const SHOT = 'shot';
export const FAULT = 'fault';
export const OFFSIDE = 'offside';
export const CUSTOM = 'custom';
export const KINDS_OF_SITUATIONS = [
    CHALLENGE_LEADING_TO_SHOT,
    ATTACKS_THROUGH_FIELD_PART,
    ATTACKS_THROUGH_TOP,
    ATTACKS_THROUGH_CENTER,
    ATTACKS_THROUGH_BOTTOM,
    COUNTERS,
    GOAL,
    CORNER,
    FREE_KICK,
    SHOT,
    FAULT,
    OFFSIDE,
    CUSTOM,
];

export class Situation {
    id: string;
    startFrame: number;
    endFrame: number;
    period: number;
    team: string;
    kind: string;

    constructor(id: string, startFrame: number, endFrame: number,
                period: number, team: string, kind: string) {
        this.id = id;
        this.startFrame = startFrame;
        this.endFrame = endFrame;
        this.period = period;
        this.team = team;
        this.kind = kind;
    }

    public static fromCustomInput(init: {
        startFrame: number, endFrame: number,
        period: number, team: string
    }) {
        return new Situation(v4(), init.startFrame, init.endFrame,
            init.period, init.team, 'custom')
    }

    public static fromEvent(event: any, kind: string, offset?: number) {
        const startFrame = offset ? event.startFrame - offset : event.startFrame;
        const endFrame = offset ? event.endFrame + offset : event.endFrame;
        return new Situation(v4(), startFrame, endFrame,
            event.period, event.team, kind);
    }

    public static fromSituationDto(situationDto: Situation) {
        return new Situation(v4(), situationDto.startFrame, situationDto.endFrame,
            situationDto.period, situationDto.team, situationDto.kind);
    }

    public compare(situation: Situation) {
        if (this.startFrame < situation.startFrame) {
            return -1;
        }
        if (this.startFrame > situation.startFrame) {
            return 1;
        }
        if (this.startFrame === situation.startFrame) {
            return 0;
        }
    }
}