<script setup lang="ts">

import { useAnimeStore } from '~/stores/anime';
import { useAuthStore } from '~/stores/auth';

const animeStore = useAnimeStore();
const authStore = useAuthStore();

onMounted(() => {
    authStore.fetchCurrentUser().then(async () => {
        await animeStore.fetchFavoriteAnimes(authStore.getCurrentUser.id);
    });
})

</script>

<template>

<div class="container">

    <h1 class="align-center">Favorites:</h1>

    <div class="anime-grid mx-auto mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        <anime-item 
            v-for="anime in animeStore.getFavoriteAnimes"
            :id="anime.id"
            :title="anime.title"
            :description="anime.description"
            :rating="anime.rating"
            :createdAt="anime.createdAt"
         />
    </div>

</div>

</template>

<style scoped>

.anime-grid {
    padding: 0 4vw;
}

</style>