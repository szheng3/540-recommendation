import {createApp} from "vue";
import {createPinia} from "pinia";

import App from "./App.vue";
import router from "./router";
import "vuetify/styles";

import {VueQueryPlugin} from "@tanstack/vue-query";
import {createVuetify} from "vuetify";
import Notifications from "@kyvg/vue3-notification";

import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import axios from "axios";

const app = createApp(App);
const vuetify = createVuetify({
  components,
  directives,
});

axios.defaults.baseURL = "http://127.0.0.1:8000";
app.use(createPinia());
app.use(router);
app.use(VueQueryPlugin);
app.use(vuetify);
app.use(Notifications);

app.mount("#app");
