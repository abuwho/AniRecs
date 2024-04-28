import { defineStore } from 'pinia'

import type { Anime } from "~/utils/types"

export const useAnimeStore = defineStore('anime', {
    state: () => {
        return {
            loading: true,
            animes: [] as Anime[]
        }
    },

    actions: {
        async fetchAnimes(query: string, jwt: string) {
            let url = `${useRuntimeConfig().public.apiBase}/animes`

            if (query.length > 0) {
                url += `?search=${query}`
            }

            try {

                this.animes = await $fetch<Anime[]>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });
            } catch (error) {
                console.error("Error fetching animes", error);
            }
        }
    },

    getters: {
        getAnimes: (state) => {
            return state.animes;
        }
    }

})