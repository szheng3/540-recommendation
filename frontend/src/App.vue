<script setup>
import {RouterView} from "vue-router";
import {computed, reactive, ref} from "vue";
import {useRouter} from "vue-router";
import {useQuery} from "@tanstack/vue-query";
import axios from "axios";

const state = reactive({
  showModal: false,
  username: "",
  userId: "",
  selectedUser: null,
  selectedName: null,
});
const links = ref(["Login"]);

const getUserInitials = computed(() => {
  if (!state.selectedName) return '';
  const nameParts = state.selectedName.split(' ');
  return nameParts.map(part => part.charAt(0).toUpperCase()).join('');
});


const {isLoading, data: users} = useQuery(
    ["author"],
    async () => {
      const response = await axios.get("/author");

      return response.data.top_authors;
    }
);


const router = useRouter();

const goToDashboard = (link) => {
  switch (link) {
    case "Login":
      state.showModal = true;
      // router.push('/')
      break;
      // case 'ONNX':
      //   router.push('/onnx')
      //   break;
    default:
      router.push("/");
  }
};

const login = () => {
  console.log(state.selectedUser);
  state.selectedName = users.value.find((user) => user.AuthorId === state.selectedUser).AuthorName;
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
            v-for="link in links"
            :key="link"
            @click="goToDashboard(link)"
            variant="text"
        >
          {{ link }}
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
          <v-card-title>Log In {{ selectedUserTitle }}</v-card-title>
          <v-card-text>
            <v-select
                v-model="state.selectedUser"
                :items="users"
                label="Select user"
                item-title="AuthorName"
                item-value="AuthorId"
            ></v-select>

            <v-text-field
                v-show="false"
                type="hidden"
                v-model="state.userId"
                style="display: none"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="state.showModal = false">Cancel</v-btn>
            <v-btn color="primary" @click="login()">Log In</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <RouterView/>
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

