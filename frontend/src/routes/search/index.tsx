import { component$ } from "@builder.io/qwik";
import type { DocumentHead } from "@builder.io/qwik-city";
import SearchBar from "~/components/search/search-bar"

export default component$(() => {
  return (
    <>
      <SearchBar />
    </>
  );
});

export const head: DocumentHead = {
  title: "AniRecs - Search",
  meta: [
    {
      name: "description",
      content: "AniRecs is an anime recommender",
    },
  ],
};
