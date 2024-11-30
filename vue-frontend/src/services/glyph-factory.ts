import {Coordinates} from "@/models/coordinates";
import {Glyph} from "@/models/glyph";
import {Player} from "@/models/player";

export class GlyphFactory {


    public static freeKick(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "freeKick.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static cornerKick(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "corner.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static yellowCard(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "yellow_card.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static redCard(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "red_card.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static shot(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.start,
            svg: "shot.svg",
            width: 20,
            height: 20,
            zIndex: 2,
            representedObject: event
        });
    }

    public static passSend(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "passSend.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static passReceived(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.startFrame,
            svg: "passReceived.svg",
            width: 12,
            height: 12,
            zIndex: 2,
            representedObject: event
        });
    }

    public static challenge(coordinates: Coordinates, event: any): Glyph {
        return new Glyph({
            coordinates,
            frame: event.endFrame,
            svg: "challenge_yellow.svg",
            width: 20,
            height: 20,
            zIndex: 3,
            representedObject: event
        });
    }

    public static playerAway(coordinates: Coordinates, player: Player): Glyph {
        return new Glyph({
            coordinates,
            frame: -1,
            svg: "player_away.svg",
            width: 16,
            height: 16,
            zIndex: 1,
            labelText: player.id,
            representedObject: player
        });
    }

    public static playerHome(coordinates: Coordinates, player: Player): Glyph {
        return new Glyph({
            coordinates,
            frame: -1,
            svg: "player_home.svg",
            width: 16,
            height: 16,
            zIndex: 1,
            labelText: player.id,
            representedObject: player
        });
    }

}