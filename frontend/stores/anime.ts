import { defineStore } from 'pinia'

import type { Anime } from "~/utils/types"

export const useAnimeStore = defineStore('anime', {
    state: () => {
        return {
            loading: true,
            animes: [] as Anime[],
            favoriteAnimes: [] as Anime[]
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
        },

        async createAnime(title: string, description: string, rating: number) {
            const url = `${useRuntimeConfig().public.apiBase}/animes`
            const jwt = localStorage.getItem('anirecs:access_token');

            try {
                const respone = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    },
                    body: JSON.stringify({
                        title,
                        description, 
                        rating
                    })
                });

                if (!respone.ok) {
                    throw new Error("Error creating anime");
                }

            } catch (error) {
                console.error("Error creating anime", error);
            }
        }, 

        async deleteAnime(animeId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/animes/${animeId}`
            const jwt = localStorage.getItem('anirecs:access_token');

            try {
                const respone = await fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    }
                });

                if (!respone.ok) {
                    throw new Error("Error deleting anime");
                }

            } catch (error) {
                console.error("Error deleting anime", error);
            }
        }, 

        async addAnimeToFavorites(animeId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/user/addfavourites`;
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    },
                    body: JSON.stringify({
                        user_id: useAuthStore().getCurrentUser.id,
                        anime_id: animeId
                    })
                });

                if (!response.ok) {
                    throw new Error("Error adding anime to favorites");
                }

            } catch (error) {
                console.error('Error adding anime to favorites', error)
            }
        },

        async fetchFavoriteAnimes(userId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/user/favourites/${userId}`
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                this.favoriteAnimes = await $fetch<Anime[]>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });

            } catch (error) {
                console.error("Error getting favorite animes", error)
            }

        }
    },

    getters: {
        getAnimes: (state) => {
            return state.animes;
        },

        getFavoriteAnimes: (state) => {
            return state.favoriteAnimes;
        }
    }

})