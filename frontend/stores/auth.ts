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
        },

        async logout() {
            const url = `${useRuntimeConfig().public.apiBase}/logout`
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Could not log out");
                }

                // Remove item in localStorage
                localStorage.removeItem('anirecs:access_token');
                this.isLoggedIn = false;
                console.log('Logout successful');

            } catch (error) {
                console.log("Error logging out: ", error);
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