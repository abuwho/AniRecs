<template>

    <div class="container">

        <h1>
            Welcome to AniRecs!
        </h1>

        <div>
            You can either
            <nuxt-link to="/auth/register"><strong> Register </strong></nuxt-link> or <nuxt-link to="/auth/login"> <strong>Log in</strong> </nuxt-link> to get started!
        </div>


    </div>

</template>

<style scoped>
.container {
    color: black;
    margin-top: 20vh;
    max-width: fit-content;
    margin-left: auto;
    margin-right: auto;
}
</style>