import {createStore} from 'vuex'
import {State} from 'vue'
import {TrajectoriesStoreObject} from "@/store/trajectories-store-object";

export default createStore<State>({
    state: {
        selectedGameDataSet: '',
        gameData: null,
        trajectories: null,
    },
    mutations: {
        updateTrajectories(state: State, trajectories: TrajectoriesStoreObject) {
            state.trajectories = trajectories;
        },
        updateGameData(state: State, gameData: any) {
            state.gameData = gameData;
        },
        updateSelectedGameDataSet(state: State, selectedGameDataSet: string) {
            state.selectedGameDataSet = selectedGameDataSet;
        }
    },
    actions: {},
    getters: {
        trajectories: state => {
            return state.trajectories;
        }
    },
    modules: {}
})