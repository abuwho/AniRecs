import { component$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";
import NavBar from "~/components/global/nav-bar"

export default component$(() => {
  return (
    <>
      <NavBar />
    </>
  );
});

export const head: DocumentHead = {
  title: "AniRecs",
  meta: [
    {
      name: "description",
      content: "AniRecs is an anime recommender",
    },
  ],
};
