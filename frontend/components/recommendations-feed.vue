<script setup lang="ts">

import { useAnimeStore } from '~/stores/anime';
const animeStore = useAnimeStore();

onMounted(async () => {
    await animeStore.fetchRecommendedAnimes();
})

</script>

<template>

    <div class="anime-grid mx-auto mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        <anime-item 
            v-for="anime in animeStore.getRecommendedAnimes"
            :id="anime.id"
            :title="anime.title"
            :description="anime.description"
            :rating="anime.rating"
            :createdAt="anime.createdAt"
         />
    </div>
    
</template>

<style scoped>

.anime-grid {
    padding: 0 4vw;
}

</style>