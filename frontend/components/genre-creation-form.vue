<script setup lang="ts">
import { useAnimeStore } from '~/stores/anime';
const animeStore = useAnimeStore();

const router = useRouter();
const nameInput = ref<HTMLInputElement | null>(null);

const handleCreateGenre = () => {
    if (nameInput.value?.value) {
        animeStore.createGenre(nameInput.value?.value as string).then(() => {
            router.push({ path: "/genres" });
        })
    }
}

</script>

<template>

    <div class="container">

        <h1 class="h1">Add new Genre</h1>

        <form action="">

            <div class="mb-3">
                <label for="name" class="form-label">Genre name</label>
                <input ref="nameInput" type="text" class="form-control" id="name" placeholder="Sci-fi">
            </div>

            <button @click="handleCreateGenre" type="button" class="btn btn-info">
                Create Genre
            </button>

        </form>
    </div>

</template>