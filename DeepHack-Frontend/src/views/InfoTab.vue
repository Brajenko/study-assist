<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <h1 style="margin-left: 1.1rem; margin-top: 2.4rem; font-weight: 700; font-size: 34px;">Справка</h1>

      <ion-grid style="margin-left: -0.65vw;">
        <ion-row>
          <ion-col size="12" size-md="4">
            <ion-card style="border-radius: 12px;">
              <ion-card-header>
                <ion-card-title>Добро пожаловать</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <ion-label>Мы рады представить Вам инновационный инструмент, который значительно упростит Вашу работу с
                  научными публикациями.

                  <b>Как это работает?</b>
                  <ol>
                    <li><b>Загрузка документа:</b> Просто загрузите интересующую Вас научную статью или исследование.
                    </li>
                    <li><b>Аннотация и ключевые пункты:</b> Наш интеллектуальный агент автоматически создаст краткую
                      выжимку, выделит основные тезисы и ключевые моменты документа.</li>
                    <li><b>Интерактивный диалог:</b> Вы можете задавать вопросы по тексту в режиме реального времени
                      через удобный чат.</li>
                    <li><b>Подробные пояснения:</b> Если какие-то фрагменты текста оставили вопросы, вы можете легко
                      выделить их и запросить детальные объяснения.</li>
                    <li><b>Генерация идей:</b> Наш агент анализирует материал и может предложить вдохновляющие идеи для
                      ваших будущих исследований, основываясь на текущих тенденциях и пробелах в исследованиях.</li>
                  </ol>




                </ion-label>
              </ion-card-content>
            </ion-card>
          </ion-col>
          <ion-col size="12" size-md="4">
            <ion-card style="border-radius: 12px;">
              <ion-card-header>
                <ion-card-title>Как начать?</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <ion-label>Все просто — загрузите нужный файл. Это может быть исследование, научная статья или любая
                  другая аналитическая или научная работа. Вы можете загрузить файл как с вашего компьютера, так и с
                  сервера, указав путь до файла в сети. Сейчас сервис работает с файлами PDF, поскольку все работы
                  распространяются именно в этом формате.

                </ion-label>
              </ion-card-content>
              <ion-card-header>
                <ion-card-title>Как я получу результат?</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <ion-label>После загузки файла, в приложении откроется специальный аналитический экран со всеми нужными
                  разделами.

                </ion-label>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonGrid, IonRow, IonCol, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonLabel, } from '@ionic/vue';
</script>