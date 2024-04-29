<script setup lang="ts">



</script>

<template>

    <div>

        <nav-bar />

        <div class="container">
            <nuxt-link to="/animes/create" type="button" class="btn btn-primary">Add a new Anime</nuxt-link>
            <anime-feed />
        </div>
    </div>

</template>