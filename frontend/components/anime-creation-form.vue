<script setup lang="ts">
import { useAnimeStore } from '~/stores/anime';
const animeStore = useAnimeStore();

const router = useRouter();
const titleInput = ref<HTMLInputElement | null>(null);
const descriptionTextArea = ref<HTMLTextAreaElement | null>(null);
const ratingInput = ref<HTMLInputElement | null>(null)
const genreInput = ref<HTMLInputElement | null>(null);

const handleCreateAnime = () => {
    if (titleInput.value?.value && descriptionTextArea.value?.value && ratingInput.value?.value && genreInput.value?.value) {
        animeStore.createAnime(titleInput.value?.value as string, descriptionTextArea.value?.value as string, ratingInput.value?.valueAsNumber, genreInput.value?.value as string).then(() => {
            router.push({ path: "/animes" });
        })
    }
}

</script>

<template>

    <div class="container">
        <h1 class="h1">Add new Anime.</h1>

            <form action="">

            <div class="mb-3">
                <label for="title" class="form-label">Title</label>
                <input ref="titleInput" type="text" class="form-control" id="title" placeholder="Naruto">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea ref="descriptionTextArea" class="form-control" id="description" rows="3"></textarea>
            </div>

            <div class="mb-3">
                <label for="rating" class="form-label">Rating</label>
                <input ref="ratingInput" type="number" class="form-control" id="rating">
            </div>

            <div class="mb-3">
                <label for="genre" class="form-label">Genre</label>
                <input ref="genreInput" type="text" class="form-control" id="genre">
            </div>

            <button @click="handleCreateAnime" type="button" class="btn btn-info">
                Create
            </button>

    </form>
    </div>

</template>