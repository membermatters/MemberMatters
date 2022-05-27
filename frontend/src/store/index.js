import { createStore } from "vuex";
import profile from "./modules/profile";
import config from "./modules/config";
import tools from "./modules/tools";
import adminTools from "./modules/adminTools";
import rfid from "./modules/rfid";
import auth from "./modules/auth";

export default createStore({
  modules: {
    profile,
    config,
    tools,
    adminTools,
    rfid,
    auth,
  },
});
