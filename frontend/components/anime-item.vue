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

            <h5 class="card-title"><strong> {{ props.title }} </strong></h5>
            <p class="card-text">{{ props.description }}</p>
            <p class="card-text">
                <strong>Rating:</strong> {{ props.rating }}⭐
            </p>

            <p class="card-text">
                <strong>ID:</strong> {{ props.id }}
            </p>

            <button @click="handleAddAnimeToFavorites" type="button" class="btn btn-info mx-2 my-2">Add to favorites</button>
            <button @click="handleDeleteAnime" class="btn btn-danger mx-2 my-2">Delete</button>
        </div>
    </div>

</template>

