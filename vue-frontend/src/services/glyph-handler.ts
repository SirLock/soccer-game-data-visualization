import {GlyphFactory} from "@/services/glyph-factory";
import {Glyph} from "@/models/glyph";
import {CoordinatesHandler} from "@/services/coordinates-handler";
import {Coordinates} from "@/models/coordinates";
import {Player} from "@/models/player";

export class GlyphHandler {
    public static addEventGlyphs(eventGlyphs: Glyph[], events: any, currentFrame: number, filter: string[]) {
        for (let event of events) {
            const currentIsNotStartOrEndFrame = event.startFrame !== currentFrame && event.endFrame !== currentFrame;
            if (currentIsNotStartOrEndFrame || !filter.includes(event.type)) {
                continue;
            }
            if (event.type === 'PASS') {
                GlyphHandler.addPassEventGlyph(eventGlyphs, event, currentFrame);
            } else if (event.type === 'CHALLENGE') {
                GlyphHandler.addChallengeEventGlyph(eventGlyphs, event);
            } else if (event.type === 'SHOT') {
                GlyphHandler.addShotEventGlyph(eventGlyphs, event);
            } else if (event.type === 'CARD') {
                if (event.subtype === 'YELLOW') {
                    GlyphHandler.addYellowCardGlyph(eventGlyphs, event);
                }
                if (event.subtype === 'RED') {
                    GlyphHandler.addRedCardGlyph(eventGlyphs, event);
                }
            } else if (event.type === 'SET PIECE') {
                if (event.subtype === 'CORNER KICK') {
                    GlyphHandler.addCornerKickGlyph(eventGlyphs, event);
                }
                if (event.subtype === 'FREE KICK') {
                    GlyphHandler.addFreeKickGlyph(eventGlyphs, event);
                }
            }
        }
    };

    public static addPlayerGlyphsFor(eventGlyphs: Glyph[],
                                     coordinates: Map<string, Coordinates>,
                                     players: Map<string, Player>,
                                     selectedEntities: string[],
                                     glyphFunction: Function) {
        selectedEntities.forEach((playerId: string) => {
            const playerCoordinates = coordinates.get(playerId);
            if (playerCoordinates && playerCoordinates.x && playerCoordinates.y) {
                eventGlyphs.push(glyphFunction(CoordinatesHandler.transformCoordinates(playerCoordinates), players.get(playerId)));
            }
        });
    };

    public static addPlayerGlyphs(eventGlyphs: Glyph[],
                                  coordinatesAway: Map<string, Coordinates>,
                                  coordinatesHome: Map<string, Coordinates>,
                                  teamsPlayers: { away: Map<string, Player>, home: Map<string, Player> },
                                  selectedEntities: { away: string[], home: string[] }) {
        GlyphHandler.addPlayerGlyphsFor(
            eventGlyphs,
            coordinatesAway,
            teamsPlayers.away,
            selectedEntities.away,
            GlyphFactory.playerAway
        );
        GlyphHandler.addPlayerGlyphsFor(
            eventGlyphs,
            coordinatesHome,
            teamsPlayers.home,
            selectedEntities.home,
            GlyphFactory.playerHome
        );
    };

    public static addPassEventGlyph(eventGlyphs: Glyph[], event: any, currentFrame: number) {
        if (currentFrame === event.startFrame) {
            GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.passSend);
        }
        if (currentFrame === event.endFrame) {
            GlyphHandler.addEventGlyph(eventGlyphs, event, event.end, GlyphFactory.passReceived);
        }
    }

    public static addChallengeEventGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.challenge);
    }

    public static addShotEventGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.shot);
    }

    public static addFreeKickGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.freeKick);
    }

    public static addCornerKickGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.cornerKick);
    }

    public static addYellowCardGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.yellowCard);
    }

    public static addRedCardGlyph(eventGlyphs: Glyph[], event: any) {
        GlyphHandler.addEventGlyph(eventGlyphs, event, event.start, GlyphFactory.redCard);
    }

    public static addEventGlyph(eventGlyphs: Glyph[], event: any, coordinates: Coordinates, glyphFunction: Function) {
        eventGlyphs.push(glyphFunction(CoordinatesHandler.transformCoordinates(coordinates), event));
    }
}