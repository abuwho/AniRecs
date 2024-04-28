<script setup lang="ts">

const props = defineProps({
    title: { type: String, default: "" },
    description: { type: String, default: "" },
    rating: { type: Number, default: 0 },
    id: { type: Number, default: 0 },
    createdAt: { type: String, default: '' }
})

</script>

<template>

    <article class="flex max-w-xl flex-col items-start justify-between">
        <div class="flex items-center gap-x-4 text-xs">
        <time :datetime="props.createdAt" class="text-gray-500">{{ props.createdAt }}</time>
            <!-- <nuxt-link :to="`/animes/${props.id}`" class="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">{{ post.category.title }}</nuxt-link> -->
        </div>
        <div class="group relative">
        <h3 class="mt-3 text-lg font-semibold leading-6 text-gray-900 group-hover:text-gray-600">
            <nuxt-link :to="`/animes/${props.id}`">
            <span class="absolute inset-0" />
            {{ props.title }}
            </nuxt-link>
        </h3>
        <p class="mt-5 line-clamp-3 text-sm leading-6 text-gray-600">{{ props.description }}</p>
        </div>
        <div class="relative mt-8 flex items-center gap-x-4">
        <nuxt-img src="/naruto.jpg" alt="Naruto" class="h-10 w-10 rounded-full bg-gray-50" />
        <div class="text-sm leading-6">
            <p class="font-semibold text-gray-900">
            <div>
                <span class="absolute inset-0" />
                Rating
                {{ props.rating }}
            </div>
            </p>
            <p class="text-gray-600">ID: {{ props.id }}</p>
        </div>
        </div>
    </article>

</template>

