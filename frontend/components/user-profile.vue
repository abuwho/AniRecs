<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
const authStore = useAuthStore();
const router = useRouter();

onMounted(async () => {
    await authStore.fetchCurrentUser();
});

const handleDeleteAccount = async () => {

    await authStore.deleteAccount();

    router.push({ path: "/" });

    authStore.$reset();

}

</script>


<template>

    <div class="container">

        <h1>Hello, 
            {{  authStore.getCurrentUser.username }}! 
            This is your profile. </h1>

        <div>Your user ID: 
            {{ authStore.getCurrentUser.id }}
        </div>

        <div>
            Profile created at: 
            {{ authStore.getCurrentUser.createdAt }}
        </div>

        <button @click="handleDeleteAccount" type="button" class="btn btn-danger">
            Delete Account
        </button>

    </div>

</template>

<style scoped>

.container {
    color: black;
  max-width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30vh;
}


</style>