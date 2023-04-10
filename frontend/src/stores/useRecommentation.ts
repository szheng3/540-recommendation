import {reactive, ref} from "vue";
import {defineStore} from "pinia";
import {useQuery} from "@tanstack/vue-query";
import axios from "axios";

export const useRecommentation = defineStore("recommendation", () => {
  const selectedCategory = ref("All");
  const state = reactive({
    recipes: [],
  });

  const fetchRecipes = async () => {
    const req = selectedCategory.value === "All" ? "" : selectedCategory.value;
    const response = await axios.get("/recipes?category=" + req);
    // state.recipes = response.data
    response.data;
  };
  // const {
  //     // data: recipes = [],
  //     status,
  //     refetch,
  // } = useQuery(["recipes"],);
  const clickCategory = async (category: string) => {
    selectedCategory.value = category;
    await fetchRecipes();
    // refetch();
  };

  const { isLoading, data: categories } = useQuery(
    ["top-categories"],
    async () => {
      const response = await axios.get("/top_categories");
      response.data.top_categories.unshift("All");

      return response.data.top_categories;
    }
  );
  return {
    categories,
    clickCategory,
    fetchRecipes,
    recipes: state.recipes,
  };
});

// import {defineStore} from "pinia";
// import axios from "axios";
//
// export const useRecommendation = defineStore("recommendation", {
//     state: () => ({
//         selectedCategory: "All",
//         categories: [],
//         recipes: [],
//     }),
//     actions: {
//         async fetchData() {
//             const req = this.selectedCategory === "All" ? "" : this.selectedCategory;
//             const data = await (await axios.get("/recipes/?category=" + req)).data;
//             this.recipes = data;
//
//             return data;
//         },
//         async fetchCategories() {
//             const response = await axios.get("/top_categories");
//             response.data.top_categories.unshift("All");
// //
// //       return response.data.top_categories;
//             this.categories = response.data.top_categories;
//             return response.data.top_categories;
//         },
//         async clickCategory(category: string) {
//             this.selectedCategory = category;
//             await this.fetchData();
//         },
//     },
// });
