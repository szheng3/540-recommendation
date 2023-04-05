<template>
  <v-container>
    <v-row>
      <v-col cols="2">
        <v-sheet rounded="lg">
          <v-list rounded="lg">

            <v-list-item
                v-for="category in categories"
                :key="category"
                link
            >
              <v-list-item-title>
                {{ category }}
              </v-list-item-title>
            </v-list-item>

            <!--            <v-divider class="my-2"></v-divider>-->

            <!--            <v-list-item-->
            <!--                link-->
            <!--                color="grey-lighten-4"-->
            <!--            >-->
            <!--              <v-list-item-title>-->
            <!--                Refresh-->
            <!--              </v-list-item-title>-->
            <!--            </v-list-item>-->
          </v-list>
        </v-sheet>
      </v-col>

      <v-col>
        <v-sheet
            min-height="70vh"
            rounded="lg"
        >
          <v-container>
            <v-row>
              <v-col v-for="(item, index) in displayedItems" :key="index" cols="12" sm="6" md="4">
                <v-card
                    :loading="true"
                    class="mx-auto "
                    max-width="374"
                >
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
                      src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
                  ></v-img>

                  <v-card-item>
                    <v-card-title>Cafe Badilico</v-card-title>

                    <v-card-subtitle>
                      <span class="me-1">Local Favorite</span>

                      <v-icon
                          color="error"
                          icon="mdi-fire-circle"
                          size="small"
                      ></v-icon>
                    </v-card-subtitle>
                  </v-card-item>

                  <v-card-text>
                    <v-row
                        align="center"
                        class="mx-0"
                    >
                      <v-rating
                          :model-value="4.5"
                          color="amber"
                          density="compact"
                          half-increments
                          readonly
                          size="small"
                      ></v-rating>

                      <div class="text-grey ms-4">
                        4.5 (413)
                      </div>
                    </v-row>

                    <div class="my-4 text-subtitle-1">
                      $ • Italian, Cafe
                    </div>

                    <!--                    <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio-->
                    <!--                      seating.-->
                    <!--                    </div>-->
                  </v-card-text>
                </v-card>

              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-pagination v-model="currentPage" :length="pageCount" @input="updateDisplayedItems"/>
              </v-col>
            </v-row>
          </v-container>

        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import {reactive, computed} from 'vue';
import {useQuery} from "@tanstack/vue-query";
import axios from "axios";


const state = reactive({
  items: [
    // Your card data here
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
  ],
  pageSize: 6,
  currentPage: 1
});

const pageCount = computed(() => {
  return Math.ceil(state.items.length / state.pageSize);
});

const displayedItems = computed(() => {
  const startIndex = (state.currentPage - 1) * state.pageSize;
  const endIndex = startIndex + state.pageSize;
  return state.items.slice(startIndex, endIndex);
});

const updateDisplayedItems = () => {
  const startIndex = (state.currentPage - 1) * state.pageSize;
  const endIndex = startIndex + state.pageSize;
  state.displayedItems = state.items.slice(startIndex, endIndex);
};

const {isLoading, data: categories} = useQuery(['top-categories'], async () => {
  const response = await axios.get("/top_categories");
  return response.data.top_categories;
});
</script>