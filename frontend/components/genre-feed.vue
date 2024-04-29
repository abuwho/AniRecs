<script setup lang="ts">

import { useAnimeStore } from '~/stores/anime';
const animeStore = useAnimeStore();

onMounted(async () => {
    await animeStore.fetchAllGenres("", localStorage.getItem('anirecs:access_token') as string);
})

</script>

<template>

    <div class="genre-grid mx-auto mt-10 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 border-t border-gray-200 pt-10 sm:mt-16 sm:pt-16 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        <genre-item 
            v-for="genre in animeStore.getGenres"
            :id="genre.id"
            :name="genre.name"
            :createdAt="genre.createdAt"
         />
    </div>
    
</template>

<style scoped>

.genre-grid {
    padding: 0 4vw;
}

</style>