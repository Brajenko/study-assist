<template>
  <ion-page>
    <ion-content :fullscreen="true">

      <ion-toast position="top" :is-open="initialLoadProgress < 2" style="--width: 32vw;"
        message="Агент анализирует данные. Осталась пара мгновений!" color="tertiary" :icon="rocketOutline">
      </ion-toast>

      <ion-popover ref="popover2" size="auto" :is-open="showMenu" style="--min-width: 270px;">
        <ion-content>
          <div style="display: flex;">
            <ion-button style="margin-left: 0.5vw; " @click="elaborate">Объяснить</ion-button>
            <ion-button style="margin-left: 0.5vw; margin-right: 0.5vw;" @click="quote_selection"
              size="auto">Цитировать</ion-button>
          </div>
        </ion-content>
      </ion-popover>

      <h1 style="margin-left: 1.1rem; margin-top: 2.4rem; font-weight: 700; font-size: 34px;">Главная</h1>
      <ion-grid>
        <ion-row>
          <ion-col style="margin-left: 0.5vw; margin-right: 2vw;">
            <ion-segment :value="currentCommonSliderTab">
              <ion-segment-button value="tab1" @click="commonSliderUpdateView('tab1')">
                <ion-label>Саммари</ion-label>
              </ion-segment-button>
              <ion-segment-button value="tab2" @click="commonSliderUpdateView('tab2')">
                <ion-label>Тезисы</ion-label>
              </ion-segment-button>
              <ion-segment-button value="tab3" @click="commonSliderUpdateView('tab3')">
                <ion-label>Анализ</ion-label>
              </ion-segment-button>
            </ion-segment>
            <transition name="fade"></transition>
            <div v-if="currentCommonSliderTab == 'tab1'">
              <div :class="summaryText === '' ? 'summary-container' : 'summary-container loading-container-justify'">
                <p v-if="summaryText != ''" class="summary-text" @mouseup.prevent="captureText" @contextmenu.prevent>
                  {{ summaryText }}
                </p>
                <p v-else class="msg-text">
                  <ion-spinner name="crescent" class="msger-loader"></ion-spinner>
                </p>

              </div>
            </div>
            <div v-if="currentCommonSliderTab == 'tab2'">
              <div>
                <ion-card v-if="!thesesAreReady" style="border-radius: 14px;">
                  <ion-card-content>
                    <ion-label><span style="color: #4f54dc">Сейчас агент анализирует предоставленный
                        материал.</span><br /><br /><i>Тезисы предоставленного вами материала появятся в течение минуты
                        (или нескольких, если загруженный файл большой).</i></ion-label>
                  </ion-card-content>
                </ion-card>

                <ion-card v-else-if="theses == null" style="border-radius: 14px;">
                  <ion-card-content>
                    <ion-label><span style="color: #4f54dc">Агент не нашел (или не вернул) ключевые точки в
                        предоставленном вами материале. Попробуйте задать интересующие вопросы в чате с
                        агентом.</span></ion-label>
                  </ion-card-content>
                </ion-card>

                <ion-card v-else class="theses-card" v-for="(thesis, index) in theses" :key="index">
                  <ion-card-content style="" id="testpopover" @mouseup.prevent="captureText" @contextmenu.prevent>
                    <div style="width: 92%;">
                      {{ thesis }}
                    </div>
                    <ion-button slot="end" class="theses-card-button" color="light" @click="quote_readytext(thesis + '')">
                      <ion-icon style="color: #4f54dc; font-size: 20px; margin: -100%; padding: -100%;"
                        :icon="scanOutline"></ion-icon>
                    </ion-button>
                    <div class="theses-gradient-line"></div>
                  </ion-card-content>
                </ion-card>
              </div>
            </div>
            <div v-if="currentCommonSliderTab == 'tab3'">
              <ion-grid>
                <ion-row>
                  <ion-col size="12" style="margin-left: -1.5vw;">
                    <h4 style="margin-left: 1vw;">Темы для продолжения этого исследования</h4>
                    <ion-card v-if="!summaryIsReady" style="border-radius: 14px;">
                      <ion-card-content>
                        <ion-label><span style="color: #4f54dc">Сейчас агент анализирует предоставленный
                            материал.</span><br /><br /><i>Глубокий анализ начнется после получения краткого содержания
                            и тезисов от агента </i></ion-label>
                      </ion-card-content>
                    </ion-card>
                    <ion-card v-else-if="futureIdeas == null" style="border-radius: 14px;">
                      <ion-card-content>
                        <ion-label><span style="color: #4f54dc">Агент занимается глубоким
                            анализом.</span><br /><br /><i>Совсем скоро данные глубокого анализа предоставленного вами
                            материала отобразятся здесь</i></ion-label>
                      </ion-card-content>
                    </ion-card>
                    <ion-card v-else class="theses-card" v-for="(idea, index) in futureIdeas" :key="index">
                      <ion-card-content style="" id="testpopover" @mouseup.prevent="captureText" @contextmenu.prevent>
                        <div style="width: 92%;">
                          {{ idea }}
                        </div>
                        <ion-button slot="end" class="theses-card-button" color="light">
                          <ion-icon style="color: #4f54dc; font-size: 20px; margin: -100%; padding: -100%;"
                            :icon="scanOutline"></ion-icon>
                        </ion-button>
                        <div class="theses-gradient-line"></div>
                      </ion-card-content>


                    </ion-card>
                  </ion-col>
                  <ion-col size="0">
                    <div>
                      <ion-card style="border-radius: 14px; text-align: center;">
                        <ion-card-content>
                          <ion-spinner style="margin-top: 4vh; margin-bottom: 4vh;" name="crescent"
                            class="msger-loader"></ion-spinner>
                        </ion-card-content>
                      </ion-card>

                    </div>

                  </ion-col>
                </ion-row>
              </ion-grid>
            </div>
          </ion-col>
          <ion-col size="12" size-md="4">
            <section class="msger">
              <header class="msger-header">
                <div class="msger-header-title">
                  <i class="fas fa-comment-alt"></i> AI Чат
                </div>
                <div class="msger-header-options">
                  <span><i class="fas fa-cog"></i></span>
                </div>
              </header>

              <main class="msger-chat">
                <div v-if="chatIsLoading">
                  <h1 style="margin-top: 15vh; text-align: center;">
                    <ion-spinner name="crescent" class="msger-loader"></ion-spinner>
                  </h1>

                </div>
                <div v-else>
                  <div v-for="(message, index) in messages" :key="index"
                    :class="message.sender === 'assistant' ? 'msg left-msg' : 'msg right-msg'">

                    <div class="msg-bubble">
                      <div class="msg-info">
                        <div class="msg-info-name">{{ message.sender === 'assistant' ? 'GPT' : 'Вы' }}</div>
                        <div class="msg-info-time">12:45</div>
                      </div>

                      <div class="msg-text" v-if="message.text != ''" v-html="message.text">

                      </div>
                      <div v-else-if="message.sender == 'assistant'" class="msg-text">
                        <ion-spinner name="crescent" class="msger-loader"></ion-spinner>
                      </div>

                    </div>
                  </div>
                </div>
              </main>

              <form class="msger-inputarea" v-on:submit.prevent="sendChatMessage">
                <input type="text" class="msger-input" v-model="newChatMessage" placeholder="Ваше сообщение...">
                <button type="submit" class="msger-send-btn">Отправить</button>
              </form>
            </section>
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonToast,
  IonLabel, IonSegment, IonSegmentButton, IonSpinner, IonPopover,
  IonGrid, IonRow, IonCol, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon,

} from '@ionic/vue';
import ExploreContainer from '@/components/ExploreContainer.vue';

import "../assets/css/chatui.css"

import "../assets/css/commonslider.css"

import { scanOutline } from 'ionicons/icons';

import { rocketOutline } from 'ionicons/icons';


export default {
  name: "app",
  components: {
    IonToast, IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonLabel, IonSegment, IonSegmentButton,
    IonGrid, IonRow, IonCol, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonButton, IonIcon,
    IonSpinner, IonPopover
  },
  data: function () {
    return {
      rocketOutline,
      scanOutline,


      fileId: "",
      initialLoading: true,
      initialLoadProgress: 0,
      summaryIsReady: false,
      thesesAreReady: false,
      chatIsLoading: false,
      currentCommonSliderTab: 'tab1',
      summaryText: ``,
      theses: null,
      futureIdeas: null,
      newChatMessage: '',
      awaitingForChatMessageReply: false,
      messages: [
        { sender: 'assistant', text: 'Смело задавайте вопросы по этой статье — на все отвечу! 😄' },
        // Add more messages here...
      ],
      selectedText: '',
      showMenu: false,
      popoverEvent: null
    };
  },
  methods: {
    //
    commonSliderUpdateView(tabId = 'tab1') {
      this.currentCommonSliderTab = tabId;
    },
    fetchInitialData() {
      // eslint-disable-next-line
      var parent_this = this;

      this.axios.get(this.$serverAddress + "/files/" + this.fileId + "/summary").then((response) => {
        console.log("Fetched data for this file: ", response.data)
        parent_this.initialLoadProgress += 1;
        parent_this.summaryText = response.data;
        parent_this.summaryIsReady = true;
        this.axios.post(this.$serverAddress + "/ideas", parent_this.summaryText).then((response) => {
          console.log("Fetched data for this file: ", response.data)
          parent_this.initialLoadProgress += 1;
          parent_this.futureIdeas = response.data;
        })
      })
      this.axios.get(this.$serverAddress + "/files/" + this.fileId + "/theses").then((response) => {
        console.log("Fetched data for this file: ", response.data)
        parent_this.initialLoadProgress += 1;
        parent_this.thesesAreReady = true;
        parent_this.theses = response.data;
      })

      setTimeout(() => {
        this.initialLoading = false;
      }, 1000);
    },
    getFutureIdeas() {
      //
    },
    sendChatMessage() {
      let newMessageText = this.newChatMessage;
      this.newChatMessage = "";
      this.processChatMessage(newMessageText)
    },
    async processChatMessage(text = "", extra_setting = null) {
      // eslint-disable-next-line
      var parent_this = this;

      this.awaitingForChatMessageReply = true;

      let elementBuilder = { sender: 'user', text: text }
      this.messages.push(elementBuilder);

      let latestMessage = this.messages[this.messages.length - 1].text;
      let finalMessagesList = null;

      if (extra_setting == "remove_html_tags") {
        let lastElProcessed = latestMessage.replace(/<[^>]*>/g, '  ');
        finalMessagesList = this.messages.slice(0, -1).concat({ sender: 'user', text: lastElProcessed })
      }

      if (finalMessagesList == null) {
        finalMessagesList = this.messages;
      }

      console.info(finalMessagesList)

      let preparedChatHistory = finalMessagesList.slice(1);

      let params = new URLSearchParams({
        'chat_history': JSON.stringify(preparedChatHistory)
      });

      let elementBuilder2 = { sender: 'assistant', text: "" }
      this.messages.push(elementBuilder2);

      fetch(`${this.$serverAddress}/files/${this.fileId}/chat/stream?file_uuid=${this.fileId}&${params.toString()}`, {
        method: 'GET',
        headers: {},
      })
        .then(response => {
          const reader = response.body.getReader();
          return new ReadableStream({
            start(controller) {
              function push() {
                reader.read().then(({ done, value }) => {
                  if (done) {
                    console.log('Stream complete');
                    let lastMessage = parent_this.messages[parent_this.messages.length - 1];
                    parent_this.messages[parent_this.messages.length - 1].text = lastMessage.text.replace(/ ▍/g, "");
                    controller.close();
                    return;
                  }
                  controller.enqueue(value);
                  let lastMessage = parent_this.messages[parent_this.messages.length - 1];
                  lastMessage.text += new TextDecoder("utf-8").decode(value);
                  console.log(lastMessage.text)
                  parent_this.messages[parent_this.messages.length - 1].text = lastMessage.text.replace(/ ▍/g, "");
                  if (!done) {
                    parent_this.messages[parent_this.messages.length - 1].text = lastMessage.text + " ▍";
                  }
                  push();
                })
              }
              push();
            }
          });
        })
        .catch(err => console.error(err));


    },
    captureText(event) {
      const selection = window.getSelection();
      this.selectedText = selection.toString();
      if (this.selectedText) {

        this.showMenu = true;
      } else {
        this.showMenu = false;
      }
    },
    elaborate() {
      this.showMenu = false;
      this.prepareElaborateChatMessage(this.selectedText);
    },
    quote_selection() {
      this.showMenu = false;
      this.prepareQuoteChatMessage(this.selectedText);
    },
    quote_readytext(text = "") {
      this.showMenu = false;
      this.prepareQuoteChatMessage(text);
    },
    prepareElaborateChatMessage(text = "") {
      // Your function here
      let preparedMessage = `<i>${text}</i><br/><br/>Что это значит? Объясни.`;
      console.log("Sending preparedMessage message to GigaChat for elaboration on it", preparedMessage);
      this.processChatMessage(preparedMessage, "remove_html_tags")
    },
    prepareQuoteChatMessage(text = "") {
      // Your function here
      let preparedMessage = `<i>${text}</i><br/><br/>Я хочу процитировать эту фразу в своей статье, напиши текст цитирования.`;
      console.log("Sending preparedMessage message to GigaChat for quotation on it", preparedMessage);
      this.processChatMessage(preparedMessage, "remove_html_tags")
    },
  },
  mounted() {
    this.fileId = this.$route.query.fileid + "";
    if (this.$route.query.fileid && this.$route.query.fileid.length > 2) {
      // ok
    } else {
      this.$router.push({ path: 'home' });
    }

    this.fetchInitialData();
  },
}
</script>
