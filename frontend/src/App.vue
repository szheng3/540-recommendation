<script setup lang="ts">
import {RouterView} from 'vue-router'
import {reactive, ref} from "vue";
import {useRouter} from 'vue-router'

const state = reactive({
  showModal: false,
  username: '',
  userId: '',
  users: [
    {id: 1, username: 'user1'},
    {id: 2, username: 'user2'},
    {id: 3, username: 'user3'},
  ],
  selectedUser: null,
});
const links = ref([
  'Login',
]);

const router = useRouter()

const goToDashboard = (link: string) => {
  switch (link) {
    case 'Login':
      state.showModal = true;
      // router.push('/')
      break;
      // case 'ONNX':
      //   router.push('/onnx')
      //   break;
    default:
      router.push('/')
  }
}


</script>


<template>
  <v-app>

    <v-app-bar flat>
      <v-container class="fill-height d-flex align-center">
        <v-avatar
            class="me-10 ms-4"
            color="grey-darken-1"
            size="32"
        ></v-avatar>

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
          <v-btn>
            Likes
          </v-btn>

        </v-responsive>
      </v-container>
    </v-app-bar>
    <notifications class="mt-10 mr-16"/>

    <v-main class="bg-grey-lighten-4">
      <v-dialog v-model="state.showModal" max-width="400px">
        <v-card>
          <v-card-title>Log In</v-card-title>
          <v-card-text>
            <v-select v-model="state.selectedUser" :items="state.users" label="Select user" item-title="username"
                      item-value="id"></v-select>

            <v-text-field v-show="false" type="hidden" v-model="state.userId" style="display: none;"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="state.showModal = false">Cancel</v-btn>
            <v-btn color="primary" @click="state.login">Log In</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <RouterView/>

    </v-main>
    <v-footer
        absolute
        class=" text-center d-flex flex-column"
        flat
    >

      <div class="text-caption">
        This project aims to show demo for recommendation system.
      </div>


      <div class="text-caption">
        {{ new Date().getFullYear() }} —Shuai, Iqra, Yiyun
      </div>
    </v-footer>
  </v-app>
</template>

<style scoped>
/*header {*/
/*  line-height: 1.5;*/
/*  max-height: 100vh;*/
/*}*/

/*.logo {*/
/*  display: block;*/
/*  margin: 0 auto 2rem;*/
/*}*/

/*nav {*/
/*  width: 100%;*/
/*  font-size: 12px;*/
/*  text-align: center;*/
/*  margin-top: 2rem;*/
/*}*/

/*nav a.router-link-exact-active {*/
/*  color: var(--color-text);*/
/*}*/

/*nav a.router-link-exact-active:hover {*/
/*  background-color: transparent;*/
/*}*/

/*nav a {*/
/*  display: inline-block;*/
/*  padding: 0 1rem;*/
/*  border-left: 1px solid var(--color-border);*/
/*}*/

/*nav a:first-of-type {*/
/*  border: 0;*/
/*}*/

/*@media (min-width: 1024px) {*/
/*  header {*/
/*    display: flex;*/
/*    place-items: center;*/
/*    padding-right: calc(var(--section-gap) / 2);*/
/*  }*/

/*  .logo {*/
/*    margin: 0 2rem 0 0;*/
/*  }*/

/*  header .wrapper {*/
/*    display: flex;*/
/*    place-items: flex-start;*/
/*    flex-wrap: wrap;*/
/*  }*/

/*  nav {*/
/*    text-align: left;*/
/*    margin-left: -1rem;*/
/*    font-size: 1rem;*/

/*    padding: 1rem 0;*/
/*    margin-top: 1rem;*/
/*  }*/
/*}*/
</style>
