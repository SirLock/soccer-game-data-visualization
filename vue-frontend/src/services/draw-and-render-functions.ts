import * as p5 from "p5";
import {Coordinates} from "@/models/coordinates";
import {CoordinatesHandler} from "@/services/coordinates-handler";
export class DrawAndRenderFunctions {

    public static drawLine(currentCoordinates: Map<string, Coordinates>,
                           nextCoordinates: Map<string, Coordinates>,
                           entity: string,
                           p5: p5) {
        const currentEntityCoords = CoordinatesHandler.getPoint(currentCoordinates, entity);
        const nextEntityCoords = CoordinatesHandler.getPoint(nextCoordinates, entity);
        if (currentEntityCoords && nextEntityCoords) {
            p5.line(
                currentEntityCoords.x,
                currentEntityCoords.y,
                nextEntityCoords.x,
                nextEntityCoords.y
            );
        }
    };

    public static drawPlayerLines(selectedPlayers: string[],
                                  currentCoordinates: Map<string, Coordinates>,
                                  nextCoordinates: Map<string, Coordinates>,
                                  p5: p5) {
        for (let player of selectedPlayers) {
            DrawAndRenderFunctions.drawLine(currentCoordinates, nextCoordinates, player, p5);
        }
    };

    public static drawBallLine(currentCoordinates: Map<string, Coordinates>,
                               nextCoordinates: Map<string, Coordinates>,
                               p5: p5) {
        DrawAndRenderFunctions.drawLine(currentCoordinates, nextCoordinates, "Ball", p5);
    };
}