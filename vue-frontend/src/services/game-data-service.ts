import {GameData} from "@/models/game-data";

export class GameDataService {
    public static gameDataService: GameDataService;

    private constructor() {
    }

    public static getInstance() {
        if (!this.gameDataService) {
            this.gameDataService = new GameDataService();
        }
        return this.gameDataService;
    }

    currentlySelectedGameDataId: string = '';
    gameDataSets: Map<string, GameData> = new Map();
    currentlyDisplayedAbsoluteFrame = -1;
    currentlyDisplayedRelativeFrame = 0;

    getGameDataSetById(id: string): GameData | undefined {
        return this.gameDataSets.get(id);
    }

    setGameData(gameData: GameData) {
        this.gameDataSets.set(gameData.id, gameData);
    }

    setCurrentlySelectedGameData(gameData: GameData) {
        this.currentlySelectedGameDataId = gameData.id;
        this.setGameData(gameData);
    }

    getCurrentlySelectedGameData() {
        return this.gameDataSets.get(this.currentlySelectedGameDataId);
    }
}