import { defineStore } from 'pinia'
import type { User } from "~/utils/types"

export const useAuthStore = defineStore('auth', {
    state: () => {
        return {
            isLoggedIn: false,
            currentUser: {} as User
        }
    },

    actions: {
        updateLoggedInStatus(newStatus: boolean) {
            this.isLoggedIn = newStatus;
        }, 

        async fetchCurrentUser() {
            const url = `${useRuntimeConfig().public.apiBase}/users/me`
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {

                this.currentUser = await $fetch<User>(url, {
                    headers: {
                        'Authorization': `Bearer ${jwt}`
                    }
                });

            } catch (error) {
                console.error("Error in fetching current user: ", error);
            }
        }
    },

    getters: {
        getIsLoggedIn: (state) => {
            return state.isLoggedIn;
        },

        getCurrentUser: (state) => {
            return state.currentUser;
        }
    }

})