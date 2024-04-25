import { component$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";
import SignupForm from "~/components/auth/signup-form"

export default component$(() => {
  return (
    <>
      <SignupForm />
    </>
  );
});

export const head: DocumentHead = {
  title: "AniRecs - Sign up",
  meta: [
    {
      name: "description",
      content: "Sign up on AniRecs",
    },
  ],
};
