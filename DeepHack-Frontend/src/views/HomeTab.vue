<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <ion-grid>
        <h1 style="margin-left: 1.4rem; margin-top: 2.4rem; font-weight: 700; font-size: 34px;">Главная</h1>
        <ion-row>

          <ion-col size="12" size-md="8">
            <ion-card style="border-radius: 18px;">
              <ion-card-header>
                <ion-card-title style="text-align: center;">Загрузить PDF файл</ion-card-title>
              </ion-card-header>

              <ion-card-content>
                <ion-label style="display: flex;
  justify-content: center;
  align-items: center;">Загрузите PDF-файл с вашего компьютера</ion-label>
                <div v-if="stage == 'init'">
                  <div id="app" style="margin-left: 5vw; margin-right: 5vw; margin-top: 3vh;">
                    <FilePond @processfile="handleFileUploaded" name="file" credits="false" allow-multiple="true"
                      max-files="1" :server="$serverAddress + '/files'" />
                  </div>
                </div>
                <div v-if="stage == 'processing'">
                  <h1>Почти готово!</h1>
                </div>
              </ion-card-content>
            </ion-card>

          </ion-col>
          <ion-col size="12" size-md="4" style="margin-left: 0vw;">
            <ion-card style="border-radius: 18px;">
              <ion-card-header>
                <ion-card-title>Указать ссылку на файл</ion-card-title>
              </ion-card-header>

              <ion-card-content>
                <ion-label>Укажите ссылку на PDF-файл</ion-label>
                <ion-item style="margin-left: -1vw; ">
                  <ion-input style="" mode="md" placeholder="https://example.com/research-paper.pdf"
                    v-model="fileonserver_input_url"></ion-input>
                </ion-item>
                <ion-button @click="accessFileByLink();" color="tertiary" expand="block"
                  style="margin-top: 2vh;">Продолжить</ion-button>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonInput,
  IonGrid, IonRow, IonCol, IonItem, IonLabel, IonCard, IonCardHeader, IonCardTitle, IonCardContent
} from '@ionic/vue';
import vueFilePond from 'vue-filepond';

// Import plugins
//@ts-ignore
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js';
//@ts-ignore
import FilePondPluginImagePreview from 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.esm.js';

// Import styles
import 'filepond/dist/filepond.min.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';

// Create FilePond component
const FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview);

export default {
  name: "app",
  components: {
    //@ts-ignore
    FilePond: vueFilePond(),
    IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
    IonButton, IonInput,
    IonGrid, IonRow, IonCol, IonItem, IonLabel, IonCard, IonCardHeader, IonCardTitle, IonCardContent
  },
  data() {
    return {
      stage: "init", fileid_onserver: null, fileurl_onserver_output: null,
      fileonserver_input_url: ""
    };
  },
  methods: {
    //
    openCommonViewPage(fileid = null) {
      this.$router.push({ path: 'results', query: { fileid: fileid } });
    },
    accessFileByLink() {
      // eslint-disable-next-line
      var parent_this = this;

      this.axios({
        method: 'post',
        url: this.$serverAddress + "/files/via_url",
        headers: { 'content-type': 'application/json' },
        data: this.fileonserver_input_url
      }).then((response) => {
        console.log("(custom file url to upload) fileId: ", response.data)
        parent_this.openCommonViewPage(response.data)
      }).catch((error) => {
        parent_this.fileonserver_input_url = "Ошибка. Попробуйте еще раз."
        setTimeout(() => {
          parent_this.fileonserver_input_url = ""
        }, 2000)
      })
    }
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    //@ts-ignore
    let parent_this = this;
    document.addEventListener('FilePond:processfile', (e) => {
      //@ts-ignore
      console.log('FilePond Widget Info: File Process Event', e.detail);
      //@ts-ignore
      if (e.detail.error == null) {
        console.log('File Uploaded Successfully.');
        //@ts-ignore
        parent_this.fileid_onserver = e.detail.file.serverId;
        //@ts-ignore
        parent_this.stage = "processing";

        // filename - e.detail.file.filename

        //@ts-ignore
        const fileid = e.detail.file.serverId;

        const cleanedFileId = fileid.replace(/[^a-zA-Z0-9]/g, '');
        parent_this.openCommonViewPage(cleanedFileId);
      }
    });
  }
};
</script>