import {Coordinates} from "@/models/coordinates";

export class CoordinatesHandler {
    public static scalingFactor = 8;
    public static borderBuffer = 25;
    public static fieldWidthMeters = 105;
    public static fieldHeightMeters = 68;
    public static fieldWidthPx = 840;
    public static fieldHeightPx = 544;

    public static getPoint(coordinates: Map<string, Coordinates>, entity: string): Coordinates | null {
        if (!coordinates || !coordinates.has(entity)) {
            return null;
        }
        // @ts-ignore
        const x = coordinates.get(entity).x;
        // @ts-ignore
        const y = coordinates.get(entity).y;
        const invalidCoordinates = !(x && y);
        if (invalidCoordinates) {
            return null;
        }
        return CoordinatesHandler.transformCoordinates(new Coordinates(x, y));
    };

    public static getGlyphAngle(originX: number, originY: number, targetX: number, targetY: number) {
        var distanceX = targetX - originX;
        var distanceY = targetY - originY;
        var angle = Math.atan2(distanceY, distanceX);
        angle *= 180 / Math.PI;
        if (angle < 0) {
            angle += 360;
        }
        return angle;
    }

    public static boundCoordinate(coordinate: number, lowerBound: number, upperBound: number): number {
        return Math.max(lowerBound, Math.min(coordinate, upperBound));
    };

    public static transformCoordinate(coordinate: number, size: number, offset: number): number {
        return Math.floor(coordinate * size) + offset;
    };

    public static transformCoordinates(coordinates: Coordinates): Coordinates {
        const transformedX = CoordinatesHandler.transformCoordinate(coordinates.x,
            CoordinatesHandler.fieldWidthPx,
            CoordinatesHandler.borderBuffer);
        const transformedY = CoordinatesHandler.transformCoordinate(coordinates.y,
            CoordinatesHandler.fieldHeightPx,
            CoordinatesHandler.borderBuffer);
        const x = CoordinatesHandler.boundCoordinate(transformedX, 0,
            CoordinatesHandler.fieldWidthPx + CoordinatesHandler.borderBuffer * 2);
        const y = CoordinatesHandler.boundCoordinate(transformedY, 0,
            CoordinatesHandler.fieldHeightPx + CoordinatesHandler.borderBuffer * 2);
        return new Coordinates(x, y);
    };

    public static determineQuadrantOfCoordinates(transformedCoordinates: Coordinates): 1 | 2 | 3 | 4 {
        const isTopHalf = transformedCoordinates.y < this.fieldHeightPx / 2;
        const isLeftHalf = transformedCoordinates.x < this.fieldWidthPx / 2;
        if (isTopHalf) {
            return isLeftHalf ? 1 : 2;
        } else {
            return isLeftHalf ? 3 : 4;
        }
    }

}