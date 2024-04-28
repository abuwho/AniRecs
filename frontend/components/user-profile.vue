<script setup lang="ts">
import { useAuthStore } from '~/stores/auth';
import { useUserStore } from '~/stores/user';

const userStore = useUserStore();
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const props = defineProps({
    perspective: { type: String, default: "" }
})

onMounted(async () => {
    if (props.perspective === 'self') {
        await authStore.fetchCurrentUser();
    }

    if (props.perspective === "others") {
        await userStore.fetchUser(+route.params.id);
    }

});

const handleDeleteAccount = async () => {

    await authStore.deleteAccount();

    router.push({ path: "/" });

    authStore.$reset();

}


const showForm = ref(false);
const toggleShowForm = () => {
    showForm.value = !showForm.value;
}

const usernameInput = ref<HTMLInputElement | null>(null);
const handleUpdateUsername = async () => {

    authStore.updateAccount(usernameInput.value?.value as string).then(() => {
        window.location.reload();
    });
}

</script>


<template>

    <div class="container">

        <h1 v-if="props.perspective === 'self'">Hello, {{  authStore.getCurrentUser.username }}! This is your profile. </h1>

        <h1 v-else-if="props.perspective === 'others'">Welcome to {{  userStore.getUser.username }}'s profile! </h1>

        <div v-if="props.perspective === 'self'">User ID: 
            {{ authStore.getCurrentUser.id }}
        </div>
        <div v-if="props.perspective === 'others'">
            User ID:
            {{ userStore.getUser.id }}
        </div>

        <div v-if="props.perspective === 'self'">
            Profile created at: 
            {{ authStore.getCurrentUser.createdAt }}
        </div>

        <div v-else="props.perspective === 'others'">
            Profile created at: 
            {{ userStore.getUser.createdAt }}
        </div>

        <button @click="toggleShowForm" v-if="props.perspective === 'self'" type="button" class="btn btn-primary">
            Edit Profile
        </button>

        <div v-if="showForm">
            <form action="">
                <label for="username">New username: </label>
                <input ref="usernameInput" id="username" type="text" placeholder="username" >
                <button @click="handleUpdateUsername" type="button" class="btn btn-success">Update username</button>
            </form>
        </div>

        <button 
            v-if="props.perspective === 'self'"
            @click="handleDeleteAccount" type="button" class="btn btn-danger">
            Delete Account
        </button>

    </div>

</template>

<style scoped>

.container {
    color: black;
  max-width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-top: 30vh;
}


</style>