<script setup lang="ts">
import { useAnimeStore } from '~/stores/anime';

const animeStore = useAnimeStore();

const props = defineProps({
    title: { type: String, default: "" },
    description: { type: String, default: "" },
    rating: { type: Number, default: 0 },
    id: { type: Number, default: 0 },
    createdAt: { type: String, default: '' }
})


const handleDeleteAnime = () => {
    animeStore.deleteAnime(props.id).then(() => {
        window.location.reload();
    });

}

const handleAddAnimeToFavorites = () => {
    animeStore.addAnimeToFavorites(props.id).then(() => {
        window.location.reload();
    })
}

</script>

<template>

    <div class="card" style="width: 18rem;">
        <img src="/naruto.jpg" class="card-img-top" alt="Naruto">
        <div class="card-body">

            <h5 class="card-title">{{ props.title }}</h5>
            <p class="card-text">{{ props.description }}</p>
            <p class="card-text">
                Rating: {{ props.rating }}⭐
            </p>

            <p class="card-text">
                ID: {{ props.id }}
            </p>

            <button @click="handleAddAnimeToFavorites" type="button" class="btn btn-info">Add to favorites</button>
            <button @click="handleDeleteAnime" class="btn btn-danger">Delete</button>
        </div>
    </div>

</template>

