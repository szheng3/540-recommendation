<script setup>
import {computed, reactive, ref, watch} from "vue";
import {useRouter} from "vue-router";
import {useQuery} from "@tanstack/vue-query";
import axios from "axios";
import {ContentLoader} from "vue-content-loader";

const state = reactive({
  showModal: false,
  username: "",
  userId: "",
  selectedUser: null,
  selectedName: null,
  selectedCategory: "All",
});
const {
  data: recipes = [],
  isLoading: recipesLoading,
  isFetching: recipesFetching,
  status,
  refetch,
} = useQuery(["recipes"], async () => {
  const req = state.selectedCategory === "All" ? "" : state.selectedCategory;
  const params = {
    category: state.selectedCategory === "All" ? "" : state.selectedCategory,
    userId: state.selectedUser,
  };
  const response = await axios.get("/recipes", {params});
  return response.data;
});
const clickCategory = (category) => {
  state.selectedCategory = category;
  refetch();
};

const {data: categories} = useQuery(["top-categories"], async () => {
  const response = await axios.get("/top_categories");
  response.data.top_categories.unshift("All");

  return response.data.top_categories;
});

const links = ref(["Login"]);

const getUserInitials = computed(() => {
  if (!state.selectedName) return "";
  const nameParts = state.selectedName.split(" ");
  return nameParts.map((part) => part.charAt(0).toUpperCase()).join("");
});

const {data: users} = useQuery(["author"], async () => {
  const response = await axios.get("/author");

  return response.data.top_authors;
});

const router = useRouter();

const goToDashboard = (link) => {
  switch (link) {
    case "Login":
      state.showModal = true;
      break;
    case "Logout":
      state.selectedUser = null;
      state.selectedName = null;
      refetch();
      break;
    default:
      router.push("/");
  }
};

const login = () => {
  state.selectedName = users.value.find(
      (user) => user.AuthorId === state.userId
  ).AuthorName;
  state.selectedUser = state.userId;
  refetch();

  state.showModal = false;
};
</script>

<template>
  <v-app>
    <v-app-bar flat>
      <v-container class="fill-height d-flex align-center">
        <v-avatar class="me-10 ms-4" color="grey-darken-1" size="32">
          <span class="text-h7">{{ getUserInitials }}</span>
        </v-avatar>

        <v-btn
            v-if="!state.selectedUser"
            @click="goToDashboard('Login')"
            variant="text"
        >
          LogIn
        </v-btn>
        <v-btn
            v-if="state.selectedUser"
            @click="goToDashboard('Logout')"
            variant="text"
        >
          LogOut
        </v-btn>

        <v-spacer></v-spacer>

        <v-responsive max-width="80">
          <v-btn> Likes</v-btn>
        </v-responsive>
      </v-container>
    </v-app-bar>
    <notifications class="mt-10 mr-16"/>

    <v-main class="bg-grey-lighten-4">
      <v-dialog v-model="state.showModal" max-width="400px">
        <v-card>
          <v-card-title>Log In</v-card-title>
          <v-card-text>
            <v-select
                v-model="state.userId"
                :items="users"
                label="Select user"
                item-title="AuthorName"
                item-value="AuthorId"
            ></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="state.showModal = false">Cancel</v-btn>
            <v-btn color="primary" @click="login()">Log In</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-container>
        <v-sheet min-height="70vh" rounded="lg" v-if="recipesLoading">
          <v-card variant="flat">
            <v-card-text class="d-flex align-content-center justify-center">
              <ContentLoader viewBox="0 0 820 450">
                <rect
                    x="10"
                    y="10"
                    rx="5"
                    ry="5"
                    width="260"
                    height="140"
                />
                <rect
                    x="280"
                    y="10"
                    rx="5"
                    ry="5"
                    width="260"
                    height="280"
                />
                <rect
                    x="550"
                    y="10"
                    rx="5"
                    ry="5"
                    width="260"
                    height="140"
                />
                <rect
                    x="10"
                    y="160"
                    rx="5"
                    ry="5"
                    width="260"
                    height="280"
                />
                <rect
                    x="280"
                    y="300"
                    rx="5"
                    ry="5"
                    width="260"
                    height="140"
                />
                <rect
                    x="550"
                    y="160"
                    rx="5"
                    ry="5"
                    width="260"
                    height="280"
                />
              </ContentLoader>
            </v-card-text>
          </v-card>
        </v-sheet>
        <v-row v-else>
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
            <v-sheet rounded="lg" v-if="recipesFetching">
              <v-card variant="flat">
                <v-card-text class="d-flex align-content-center justify-center">
                  <ContentLoader viewBox="0 0 820 450">
                    <rect
                        x="10"
                        y="10"
                        rx="5"
                        ry="5"
                        width="260"
                        height="140"
                    />
                    <rect
                        x="280"
                        y="10"
                        rx="5"
                        ry="5"
                        width="260"
                        height="280"
                    />
                    <rect
                        x="550"
                        y="10"
                        rx="5"
                        ry="5"
                        width="260"
                        height="140"
                    />
                    <rect
                        x="10"
                        y="160"
                        rx="5"
                        ry="5"
                        width="260"
                        height="280"
                    />
                    <rect
                        x="280"
                        y="300"
                        rx="5"
                        ry="5"
                        width="260"
                        height="140"
                    />
                    <rect
                        x="550"
                        y="160"
                        rx="5"
                        ry="5"
                        width="260"
                        height="280"
                    />
                  </ContentLoader>
                </v-card-text>
              </v-card>
            </v-sheet>
            <v-sheet min-height="70vh" rounded="lg" v-else>
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
                      ></v-img>

                      <v-card-item>
                        <v-card-title>{{ item.Name }}</v-card-title>

                        <v-card-subtitle>
                          <span class="me-1">
                            Calories: {{ item.Calories }}
                          </span>
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
    </v-main>
    <v-footer absolute class="text-center d-flex flex-column" flat>
      <div class="text-caption">
        This project aims to show demo for recommendation system.
      </div>

      <div class="text-caption">
        {{ new Date().getFullYear() }} —Shuai, Iqra, Yiyun
      </div>
    </v-footer>
  </v-app>
</template>
