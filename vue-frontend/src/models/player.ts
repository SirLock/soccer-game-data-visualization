export class Player {
    id: string;
    name: string;
    team: string;
    
    constructor(init: Player) {
        this.id = init.id;
        this.name = init.name;
        this.team = init.team;
    }
}