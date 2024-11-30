export class BasicGameInformation {
    firstPeriodEnd: number;
    secondPeriodStart: number;

    constructor(init: BasicGameInformation) {
        this.firstPeriodEnd = init.firstPeriodEnd;
        this.secondPeriodStart = init.secondPeriodStart;
    }
}