import { component$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";
import LoginForm from "~/components/auth/login-form"

export default component$(() => {
  return (
    <>
      <LoginForm />
    </>
  );
});

export const head: DocumentHead = {
  title: "AniRecs - Login",
  meta: [
    {
      name: "description",
      content: "Log in to AniRecs",
    },
  ],
};
