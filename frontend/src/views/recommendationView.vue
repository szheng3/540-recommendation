<template></template>

<script setup>
import {ref} from "vue";
import {useQuery} from "@tanstack/vue-query";
import axios from "axios";

const selectedCategory = ref("All");

const {
  data: recipes = [],
  status,
  refetch,
} = useQuery(["recipes"], async () => {
  const req = selectedCategory.value === "All" ? "" : selectedCategory.value;
  const response = await axios.get("/recipes/?category=" + req);
  return response.data;
});
const clickCategory = (category) => {
  selectedCategory.value = category;
  refetch();
};

const { isLoading, data: categories } = useQuery(
  ["top-categories"],
  async () => {
    const response = await axios.get("/top_categories");
    response.data.top_categories.unshift("All");

    return response.data.top_categories;
  }
);
</script>
