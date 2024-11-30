import {FrameElement} from "@/models/frame-element";

export const EVENT_PASS = 'PASS';
export const EVENT_CHALLENGE = 'CHALLENGE';
export const EVENT_SHOT = 'SHOT';
export const EVENT_CARD = 'CARD';
export const EVENT_CARD_YELLOW = 'YELLOW';
export const EVENT_CARD_RED = 'RED';
export const EVENT_SET_PIECE_FREE_KICK = 'FREE KICK';
export const EVENT_SET_PIECE_CORNER_KICK = 'CORNER KICK';

export const EVENT_SVG_MAPPINGS = {
    'PASS': 'passSend.svg',
    'CHALLENGE': 'challenge_yellow.svg',
    'SHOT': 'shot.svg',
    'YELLOW': 'yellow_card.svg',
    'RED': 'red_card.svg',
    'FREE KICK': 'freeKick.svg',
    'CORNER KICK': 'corner.svg',
}

export const EVENT_ALL = [
    EVENT_PASS,
    EVENT_CHALLENGE,
    EVENT_SHOT,
    EVENT_CARD_YELLOW,
    EVENT_CARD_RED,
    EVENT_SET_PIECE_FREE_KICK,
    EVENT_SET_PIECE_CORNER_KICK
]

export class Events {
    allEvents: FrameElement[];
    shots: Event;
    passes: Event;
    challenges: Event;
    freekicks: Event;
    throwins: Event;
    kickoffs: Event;
    corners: Event;
    ballouts: Event;
    faults: Event;
    cards: Event;
    ballLostEvents: Event;

    public constructor(init: any) {
        this.allEvents = init?.team;
        this.shots = init?.type;
        this.passes = init?.subtype;
        this.challenges = init?.period;
        this.freekicks = init?.startFrame;
        this.throwins = init?.startTime;
        this.kickoffs = init?.endFrame;
        this.corners = init?.endTime;
        this.ballouts = init?.origin;
        this.faults = init?.target;
        this.cards = init?.start;
        this.ballLostEvents = init?.endFrame;
    }
}