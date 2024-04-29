<script setup lang="ts">

import { useAuthStore } from '~/stores/auth';
const authStore = useAuthStore();

onMounted(async () => {

    await authStore.fetchCurrentUser();

})

</script>

<template>
    <div>
        <nav-bar />
        <div class="container">


            <h1>Recommended animes for @ {{ authStore.getCurrentUser.username }}</h1>

            <anime-feed />

        </div>
    </div>

</template>