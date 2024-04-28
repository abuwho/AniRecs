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
        }, 

        async updateAccount(newUsername: string) {
            const url = `${useRuntimeConfig().public.apiBase}/users/${this.currentUser.id}`;
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                const response = await fetch(url, {
                    method: 'PUT', 
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    }, 
                    body: JSON.stringify({
                        username: newUsername
                    })
                });

                if (!response.ok) {
                    throw new Error("Error updating account.");
                }

                console.log("Updated username successfully.")
            } catch (error) {
                console.error("Error updating account.", error)
            }
        },

        async deleteAccount() {
            const url = `${useRuntimeConfig().public.apiBase}/users/me`;
            const jwt = localStorage.getItem('anirecs:access_token') as string;

            try {
                const response = await fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwt}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Could not delete account");
                }

                // Remove item in localStorage
                localStorage.removeItem('anirecs:access_token');
                this.isLoggedIn = false;
                console.log('Account deleted successfully');

            } catch (error) {
                console.log("Error deleting account: ", error);
            }

        }, 
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