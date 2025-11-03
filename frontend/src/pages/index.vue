<script setup lang="ts">
const appConfig = useAppConfig();
useSeoMeta({ titleTemplate: appConfig.title });

definePageMeta({ layout: 'default' });

const api = useApi();
const { data, pending, error, execute } = await useAsyncData(
  'users',
  () => api.user.getUsers(),
  { immediate: false }
);

onMounted(() => {
  if (!data.value) execute();
});
</script>

<template>
  <UCard>
    <h1 class="mb-4 text-2xl font-bold">Danh sách người dùng</h1>

    <div v-if="pending" class="text-center">
      <UButton loading />
    </div>

    <div v-else-if="error" class="text-red-500">Lỗi: {{ error.message }}</div>

    <ul v-else-if="data" class="space-y-2">
      <li v-for="user in data" :key="user.id" class="rounded bg-gray-50 p-3">
        {{ user.name }} ({{ user.email }})
        <NuxtLink :to="`/users/${user.id}`">
          <UButton size="xs" color="primary">Xem</UButton>
        </NuxtLink>
      </li>
    </ul>
  </UCard>
</template>
