<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
</script>

<style>

ion-content {
    --background: #ffffff00 no-repeat center center / cover !important;
}

</style>
