<!--
  Copyright 2025 Haui.HIT - H2K
  Licensed under the Apache License, Version 2.0
  http://www.apache.org/licenses/LICENSE-2.0
-->

<script setup lang="ts">
const appConfig = useAppConfig();
useHead({ titleTemplate: `%s | ${appConfig.title}` });

const toaster = { position: 'top-right' };
</script>
<template>
  <UApp :toaster="toaster">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
