<template>
  <v-container>
    <v-row>
      <v-col cols="2">
        <v-sheet rounded="lg">
          <v-list rounded="lg">
            <v-list-subheader>Category</v-list-subheader>

            <v-list-item
              v-for="(category, i) in categories"
              :key="i"
              :value="category"
              active-color="primary"
              rounded="shaped"
              @click="clickCategory(category)"
              link
            >
              <v-list-item-title>
                {{ category }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet min-height="70vh" rounded="lg">
          <v-container>
            <v-row>
              <v-col
                v-for="(item, index) in recipes"
                :key="index"
                cols="12"
                sm="6"
                md="4"
              >
                <v-card :loading="false" class="mx-auto" max-width="374">
                  <template v-slot:loader="{ isActive }">
                    <v-progress-linear
                      :active="isActive"
                      color="deep-purple"
                      height="4"
                      indeterminate
                    ></v-progress-linear>
                  </template>

                  <v-img
                    cover
                    height="250"
                    :src="item.first_image_url"
                    lazy-src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
                  ></v-img>

                  <v-card-item>
                    <v-card-title>{{ item.Name }}</v-card-title>

                    <v-card-subtitle>
                      <span class="me-1"> Calories: {{ item.Calories }} </span>
                      <!--                      <span class="me-1"> {{item.RecipeCategory}} </span>-->

                      <v-icon
                        color="error"
                        icon="mdi-fire-circle"
                        size="small"
                      ></v-icon>
                    </v-card-subtitle>
                  </v-card-item>

                  <v-card-text>
                    <v-row align="center" class="mx-0">
                      <v-rating
                        v-model="item.AggregatedRating"
                        color="amber"
                        density="compact"
                        half-increments
                        readonly
                        size="small"
                      ></v-rating>

                      <div class="text-grey ms-4">
                        {{ item.AggregatedRating }} ({{ item.ReviewCount }})
                      </div>
                    </v-row>

                    <div class="my-4 text-subtitle-1">
                      {{ item.RecipeCategory }}
                    </div>

                    <!--                    <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio-->
                    <!--                      seating.-->
                    <!--                    </div>-->
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useQuery } from "@tanstack/vue-query";
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
