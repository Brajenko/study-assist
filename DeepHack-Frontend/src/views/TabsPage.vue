<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="tab1" href="/tabs/home">
          <ion-icon aria-hidden="true" :icon="prismOutline" />
          <ion-label>Приложение</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="tab2" href="/tabs/info">
          <ion-icon aria-hidden="true" :icon="receiptOutline" />
          <ion-label>Справка</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { prismOutline, receiptOutline } from 'ionicons/icons';
</script>
