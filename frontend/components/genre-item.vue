<script setup lang="ts">
import { useAnimeStore } from '~/stores/anime';

const animeStore = useAnimeStore();

const props = defineProps({
    name: { type: String, default: "" },
    id: { type: Number, default: 0 },
    createdAt: { type: String, default: '' }
})


const handleDeleteGenre = () => {
    animeStore.deleteGenre(props.id).then(() => {
        window.location.reload();
    });
}

const handleAddGenreToPreferences = () => {
    animeStore.addGenreToPreferences(props.id).then(() => {
        window.location.reload();
    })
}

</script>

<template>

    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">{{ props.name }}</h5>
            <p class="card-text">
                ID: {{ props.id }}
            </p>

            <button @click="handleAddGenreToPreferences" type="button" class="btn btn-info">Add to preferences</button>
            <button @click="handleDeleteGenre" class="btn btn-danger">Delete genre</button>
        </div>
    </div>

</template>

