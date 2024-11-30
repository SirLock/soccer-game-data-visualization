import {Store} from '@/typings/vuex'
import {TrajectoriesStoreObject} from "@/store/trajectories-store-object";

declare module '@vue/runtime-core' {

    interface State {
        selectedGameDataSet: string,
        gameData: any,
        trajectories: TrajectoriesStoreObject | null
    }

    interface ComponentCustomProperties {
        $store: Store<State>
        $emit: never,
        $refs: never
    }
}