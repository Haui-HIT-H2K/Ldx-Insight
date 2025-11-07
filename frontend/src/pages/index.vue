<script setup lang="ts">
const appConfig = useAppConfig();
useSeoMeta({ titleTemplate: appConfig.title });
definePageMeta({ layout: 'default' });

const router = useRouter();
const q = ref('');
const filters = [
  {
    title: 'Tất cả',
    category: '',
  },
  { title: 'Văn hoá du lịch', category: 'Văn hoá du lịch' },
  { title: 'Giáo dục', category: 'Giáo dục' },
  { title: 'Kinh tế', category: 'Kinh tế' },
];

const api = useApi();
const { data: summaryRes } = await useAsyncData(
  'statsSummary',
  () => api.stats.summary(),
  {
    immediate: true,
  }
);

const { data: topViewed, pending: topViewedPending } = await useAsyncData(
  'topViewed',
  () => api.stats.topViewed(10)
);

const { data: topDownloaded, pending: topDownloadedPending } =
  await useAsyncData('topDownloaded', () => api.stats.topDownloaded(6));

const { data: categoryStats, pending: categoryStatsPending } =
  await useAsyncData('categoryStats', () => api.stats.byCategory());

const onSearch = () => {
  if (!q.value) return;
  router.push({
    path: '/data',
    query: { q: q.value },
  });
};

const navigateToCategory = (category: string) => {
  router.push({
    path: '/data',
    query: { category: category },
  });
};
</script>

<template>
  <div
    class="from-primary via-accent to-secondary text-primary-foreground flex h-screen flex-col items-center justify-center bg-linear-to-br py-20"
  >
    <div class="mx-auto px-4 text-white sm:px-6 lg:px-8">
      <div class="mb-12 text-center">
        <h1 class="mb-4 text-5xl font-bold">Open Linked Hub</h1>
        <p class="mb-8 text-xl opacity-90">
          Khám phá, tìm hiểu và truy cập các bộ dữ liệu công khai
        </p>
      </div>

      <div class="mx-auto mb-12 max-w-2xl">
        <div class="flex gap-2">
          <div class="relative flex-1 rounded-3xl">
            <Icon
              name="lucide:search"
              class="absolute top-3.5 left-4 h-5 w-5 opacity-50"
            />
            <input
              v-model="q"
              type="text"
              placeholder="Tìm kiếm dữ liệu..."
              class="bg-primary-foreground text-foreground placeholder-muted-foreground focus:ring-accent w-full rounded-3xl border-2 py-3 pr-4 pl-12 focus:ring-1 focus:outline-none"
              @keydown.enter="onSearch"
            />
          </div>
          <UButton
            class="cursor-pointer rounded-3xl px-8 text-base"
            @click="onSearch"
          >
            Tìm kiếm
          </UButton>
        </div>
      </div>

      <div class="flex flex-wrap justify-center gap-3">
        <UButton
          v-for="filter in filters"
          :key="filter.category"
          color="neutral"
          variant="outline"
          class="hover:bg-primary/30 cursor-pointer rounded-3xl bg-transparent px-4 text-white"
          @click="navigateToCategory(filter.category)"
        >
          {{ filter.title }}
        </UButton>
      </div>
    </div>

    <div class="mt-10 flex justify-center">
      <div class="flex justify-items-center gap-10">
        <div
          class="border-primary flex flex-col justify-start gap-4 rounded-2xl border-2 bg-white/70 p-6 px-12 text-center text-black/70 shadow"
        >
          <p class="text-5xl font-bold" v-if="summaryRes?.totalDatasets">
            {{ summaryRes?.totalDatasets }}
          </p>
          <UIcon
            name="line-md:loading-loop"
            class="text-primary size-12"
            v-else
          />
          <div class="flex items-center gap-2">
            <UIcon name="icon-park-outline:data" class="size-5" />
            <p>Dữ liệu</p>
          </div>
        </div>
        <div
          class="border-primary flex flex-col justify-start gap-4 rounded-2xl border-2 bg-white/70 p-6 px-12 text-center text-black/70 shadow"
        >
          <p class="text-5xl font-bold" v-if="summaryRes?.totalViews">
            {{ summaryRes?.totalViews }}
          </p>
          <UIcon
            name="line-md:loading-loop"
            class="text-primary size-12"
            v-else
          />
          <div class="flex items-center gap-2">
            <UIcon name="lucide:eye" class="size-5" />
            <p>Số lượt xem</p>
          </div>
        </div>
        <div
          class="border-primary flex flex-col justify-start gap-4 rounded-2xl border-2 bg-white/70 p-6 px-12 text-center text-black/70 shadow"
        >
          <p class="text-5xl font-bold" v-if="summaryRes?.totalDownloads">
            {{ summaryRes?.totalDownloads }}
          </p>
          <UIcon
            name="line-md:loading-loop"
            class="text-primary size-12"
            v-else
          />
          <div class="flex items-center gap-2">
            <UIcon name="lucide:download" class="size-5" />
            <p>Số lượt tải</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <section class="bg-gray-50 py-16">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <h2 class="mb-12 text-center text-3xl font-bold text-gray-800">
        Thống kê chi tiết
      </h2>

      <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <UCard class="lg:col-span-2">
          <template #header>
            <h3 class="text-lg font-semibold">
              Dữ liệu theo danh mục (Top 10)
            </h3>
          </template>

          <div
            v-if="categoryStatsPending"
            class="flex h-72 items-center justify-center"
          >
            <UIcon name="line-md:loading-loop" class="text-primary size-8" />
          </div>
          <!-- <BarChart
            :data="RevenueData"
            :height="300"
            :categories="RevenueCategories"
            :y-axis="['desktop']"
            :x-num-ticks="6"
            :radius="4"
            :y-grid-line="true"
            :x-formatter="xFormatter"
            :y-formatter="yFormatter"
            :legend-position="LegendPosition.TopRight"
            :hide-legend="false"
          /> -->
        </UCard>

        <UCard>
          <template #header>
            <h3 class="text-lg font-semibold">Tải nhiều nhất</h3>
          </template>

          <div
            v-if="topDownloadedPending"
            class="flex h-72 items-center justify-center"
          >
            <UIcon name="line-md:loading-loop" class="text-primary size-8" />
          </div>
          <ul v-else-if="topDownloaded" class="h-72 space-y-3 overflow-y-auto">
            <li
              v-for="item in topDownloaded.slice(0, 10)"
              :key="item.id"
              class="flex items-start justify-between gap-2"
            >
              <NuxtLink
                :to="`/data/${item.id}`"
                class="hover:text-primary text-sm font-medium wrap-break-word"
              >
                {{ item.title }}
              </NuxtLink>
              <UBadge color="gray" variant="soft" class="shrink-0">
                <UIcon name="lucide:download" class="mr-1" />
                {{ item.downloadCount }}
              </UBadge>
            </li>
          </ul>
        </UCard>

        <UCard class="lg:col-span-3">
          <template #header>
            <h3 class="text-lg font-semibold">Xem nhiều nhất (Top 10)</h3>
          </template>

          <div
            v-if="topViewedPending"
            class="flex h-72 items-center justify-center"
          >
            <UIcon name="line-md:loading-loop" class="text-primary size-8" />
          </div>
          <ul v-else-if="topViewed" class="h-72 space-y-3 overflow-y-auto pr-3">
            <li
              v-for="item in topViewed.slice(0, 10)"
              :key="item.id"
              class="flex items-center justify-between gap-4 border-b pb-2"
            >
              <NuxtLink
                :to="`/data/${item.id}`"
                class="hover:text-primary font-medium"
              >
                {{ item.title }}
              </NuxtLink>
              <div class="flex shrink-0 gap-4">
                <span class->
                  <UIcon name="lucide:eye" class="text-muted-foreground mr-1" />
                  {{ item.viewCount }}
                </span>
                <span class->
                  <UIcon
                    name="lucide:download"
                    class="text-muted-foreground mr-1"
                  />
                  {{ item.downloadCount }}
                </span>
              </div>
            </li>
          </ul>
        </UCard>
      </div>
    </div>
  </section>
</template>
