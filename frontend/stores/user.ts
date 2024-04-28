import { defineStore } from 'pinia'
import type { User } from "~/utils/types"

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            user: {} as User
        }
    },

    actions: {

        async fetchUser(userId: number) {
            const url = `${useRuntimeConfig().public.apiBase}/users/${userId}`
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {

                this.user = await $fetch<User>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });

            } catch (error) {
                console.error("Error fetching user: ", error);
            }
        },
        
    },

    getters: {
        getUser: (state) => {
            return state.user;
        },
    }

})