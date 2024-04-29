import { defineStore } from 'pinia'

import type { Anime, Genre } from "~/utils/types"

export const useAnimeStore = defineStore('anime', {
    state: () => {
        return {
            loading: true,
            animes: [] as Anime[],
            genres: [] as Genre[],
            favoriteAnimes: [] as Anime[],
            recommendedAnimes: [] as Anime[]
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

        },

        async fetchRecommendedAnimes() {
            const url = `${useRuntimeConfig().public.apiBase}/recommendations`;
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                this.recommendedAnimes = await $fetch<Anime[]>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });
            } catch (error) {
                console.error("Error fetching recommended animes", error)
            }
        },

        async createGenre(name: string) {
            const url = `${useRuntimeConfig().public.apiBase}/genres`;
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                const respone = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    },
                    body: JSON.stringify({ name })
                });

                if (!respone.ok) {
                    throw new Error("Error creating genre");
                }

            } catch (error) {
                console.error("Error creating genre", error);
            }
        }, 

        async fetchAllGenres(query: string, jwt: string) {
            let url = `${useRuntimeConfig().public.apiBase}/genres`

            if (query.length > 0) {
                url += `?search=${query}`
            }

            try {

                this.genres = await $fetch<Genre[]>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });
            } catch (error) {
                console.error("Error fetching genres", error);
            }
        },

        async addGenreToPreferences(genreId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/user/addpreferences`;
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
                        genre_id: genreId
                    })
                });

                if (!response.ok) {
                    throw new Error("Error adding anime to favorites");
                }

            } catch (error) {
                console.error('Error adding anime to favorites', error)
            }
        },

        async deleteGenre(genreId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/genres/${genreId}`
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
                    throw new Error("Error deleting genre");
                }

            } catch (error) {
                console.error("Error deleting genre", error);
            }
        }, 

    },

    getters: {
        getAnimes: (state) => {
            return state.animes;
        },

        getGenres: (state) => {
            return state.genres;
        },

        getFavoriteAnimes: (state) => {
            return state.favoriteAnimes;
        },

        getRecommendedAnimes: (state) => {
            return state.recommendedAnimes;
        }
    }

})