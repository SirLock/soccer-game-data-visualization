export class FieldPart {
    minX: number;
    maxX: number;
    minY: number;
    maxY: number;

    constructor(minX: number, maxX: number, minY: number, maxY: number) {
        this.minX = minX;
        this.maxX = maxX;
        this.minY = minY;
        this.maxY = maxY;
    }
}

export const LEFT_UPPER = new FieldPart(0, 0.33, 0 / 9.1, 2 / 9.1)
export const LEFT_UPPERMID = new FieldPart(0, 0.33, 2 / 9.1, 3.4 / 9.1)
export const LEFT_MID = new FieldPart(0, 0.33, 3.4 / 9.1, 5.7 / 9.1)
export const LEFT_LOWERMID = new FieldPart(0, 0.33, 5.7 / 9.1, 7.1 / 9.1)
export const LEFT_LOWER = new FieldPart(0, 0.33, 7.1 / 9.1, 9.1 / 9.1)
export const CENTER_UPPER = new FieldPart(0.33, 0.66, 0 / 9.1, 2 / 9.1)
export const CENTER_UPPERMID = new FieldPart(0.33, 0.66, 2 / 9.1, 3.4 / 9.1)
export const CENTER_MID = new FieldPart(0.33, 0.66, 3.4 / 9.1, 5.7 / 9.1)
export const CENTER_LOWERMID = new FieldPart(0.33, 0.66, 5.7 / 9.1, 7.1 / 9.1)
export const CENTER_LOWER = new FieldPart(0.33, 0.66, 7.1 / 9.1, 9.1 / 9.1)
export const RIGHT_UPPER = new FieldPart(0.66, 1, 0 / 9.1, 2 / 9.1)
export const RIGHT_UPPERMID = new FieldPart(0.66, 1, 2 / 9.1, 3.4 / 9.1)
export const RIGHT_MID = new FieldPart(0.66, 1, 3.4 / 9.1, 5.7 / 9.1)
export const RIGHT_LOWERMID = new FieldPart(0.66, 1, 5.7 / 9.1, 7.1 / 9.1)
export const RIGHT_LOWER = new FieldPart(0.66, 1, 7.1 / 9.1, 9.1 / 9.1)
export const RIGHT_HALF = new FieldPart(0.5, 1, 0, 1)
export const LEFT_HALF = new FieldPart(0, 0.5, 0, 1)
export const UPPER_RIGHT_HALF = new FieldPart(0.5, 1, 0, 1)