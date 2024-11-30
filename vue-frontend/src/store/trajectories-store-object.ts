import {Glyph} from "@/models/glyph";

export class TrajectoriesStoreObject {
    situations: any[] | undefined;
    eventsToDisplay: any[] | undefined;
    eventGlyphsToDisplay: Glyph[] | undefined;
    teamsSelectedPlayers: string[] | undefined;
    teamsPlayerOptions: string[] | undefined;
    displayedSituationIndex: number | undefined;
    situationFilter: { selectedTeams: string[], selectedSituations: string[] } | undefined;

    constructor(init: Partial<TrajectoriesStoreObject>) {
        this.situations = init.situations;
        this.eventsToDisplay = init.eventsToDisplay;
        this.eventGlyphsToDisplay = init.eventGlyphsToDisplay;
        this.teamsSelectedPlayers = init.teamsSelectedPlayers;
        this.teamsPlayerOptions = init.teamsPlayerOptions;
        this.displayedSituationIndex = init.displayedSituationIndex;
        this.situationFilter = init.situationFilter;
    }


}