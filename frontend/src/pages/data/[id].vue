<script setup lang="ts">
definePageMeta({ layout: 'default' });

const route = useRoute();
const datasetId = computed(() => route.params.id);
const isDownloading = ref(false);

const api = useApi();
const { data: detailRes } = await useAsyncData(
  'detailDataset',
  () => api.dataset.detail(datasetId.value as string),
  {
    immediate: true,
  }
);

await useAsyncData(
  'viewDataset',
  () => api.dataset.viewData(datasetId.value as string),
  { immediate: true }
);

async function onDownload() {
  if (isDownloading.value) return;
  isDownloading.value = true;

  try {
    const response = await api.dataset.download(datasetId.value as string);

    const blob = await response.blob();

    const contentDisposition = response.headers.get('content-disposition');
    let filename = `dataset-${datasetId.value}.zip`;

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+?)"?$/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1];
      }
    }

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    a.remove();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Download failed:', error);
    isDownloading.value = false;
  }
}

useSeoMeta({
  title: () => (detailRes.value ? detailRes.value?.title : 'Dataset not found'),
  description: () => detailRes.value?.description ?? 'Dataset detail',
});
</script>

<template>
  <div>
    <main class="bg-background min-h-screen">
      <!-- Not found -->
      <section
        v-if="!detailRes"
        class="flex min-h-[60vh] items-center justify-center"
      >
        <div class="text-center">
          <h1 class="mb-4 text-2xl font-bold">Không tìm thấy dữ liệu</h1>
          <NuxtLink to="/data" class="text-primary hover:underline">
            Quay lại
          </NuxtLink>
        </div>
      </section>

      <!-- Header -->
      <section
        v-else
        class="from-primary via-accent to-secondary text-primary-foreground bg-linear-to-r py-8"
      >
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <NuxtLink
            to="/data"
            class="mb-4 flex w-fit items-center gap-2 transition-opacity hover:opacity-80"
          >
            <Icon name="lucide:arrow-left" class="h-5 w-5" />
            <span>Quay lại</span>
          </NuxtLink>
          <h1 class="mb-2 text-4xl font-bold text-white">
            {{ detailRes.title }}
          </h1>
          <p class="text-lg text-white opacity-90">
            {{ detailRes.source }}
          </p>
        </div>
      </section>

      <!-- Content -->
      <div
        v-if="detailRes"
        class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8"
      >
        <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
          <!-- Main Content -->
          <div class="space-y-8 lg:col-span-2">
            <!-- Overview -->
            <div class="bg-card border-border rounded-lg border p-6">
              <h2 class="mb-4 text-2xl font-bold">Tổng quát</h2>
              <div
                class="text-muted-foreground whitespace-pre-line"
                v-html="detailRes.description"
              ></div>
            </div>

            <!-- Data Structure -->
            <!-- <div class="bg-card border-border rounded-lg border p-6">
              <h2 class="mb-4 text-2xl font-bold">Data Structure</h2>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="border-border border-b">
                      <th class="px-4 py-3 text-left font-semibold">
                        Column Name
                      </th>
                      <th class="px-4 py-3 text-left font-semibold">
                        Data Type
                      </th>
                      <th class="px-4 py-3 text-left font-semibold">
                        Description
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(col, idx) in detailRes.dataColumns"
                      :key="idx"
                      class="border-border hover:bg-muted/50 border-b"
                    >
                      <td class="text-primary px-4 py-3 font-mono">
                        {{ col.name }}
                      </td>
                      <td class="text-muted-foreground px-4 py-3">
                        {{ col.type }}
                      </td>
                      <td class="text-muted-foreground px-4 py-3">
                        {{ col.description }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div> -->
          </div>

          <!-- Sidebar -->
          <div class="space-y-6 lg:col-span-1">
            <!-- Quick Stats -->
            <div class="bg-card border-border rounded-lg border p-6">
              <h3 class="mb-4 text-lg font-bold">Statistics</h3>
              <div class="space-y-4">
                <div class="flex items-center gap-3">
                  <Icon name="lucide:download" class="text-primary h-5 w-5" />
                  <div>
                    <p class="text-muted-foreground text-sm">Lượt tải</p>
                    <p class="font-bold">
                      {{ detailRes.downloadCount }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <Icon name="lucide:eye" class="text-primary h-5 w-5" />
                  <div>
                    <p class="text-muted-foreground text-sm">Lượt xem</p>
                    <p class="font-bold">
                      {{ detailRes.viewCount }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center gap-3">
                  <Icon name="lucide:calendar" class="text-primary h-5 w-5" />
                  <div>
                    <p class="text-muted-foreground text-sm">
                      Lần cập nhật cuối
                    </p>
                    <p class="font-bold">{{ detailRes.updatedAt }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dataset Info -->
            <div class="bg-card border-border rounded-lg border p-6">
              <h3 class="mb-4 text-lg font-bold">Thông tin dữ liệu</h3>
              <div class="space-y-3 text-sm">
                <div>
                  <p class="text-muted-foreground">Danh mục</p>
                  <p class="text-primary font-semibold">
                    {{ detailRes.category }}
                  </p>
                </div>
                <!-- <div>
                  <p class="text-muted-foreground">Format</p>
                  <p class="font-semibold">{{ detailRes.format }}</p>
                </div>
                <div>
                  <p class="text-muted-foreground">File Size</p>
                  <p class="font-semibold">{{ detailRes.fileSize }}</p>
                </div>
                <div>
                  <p class="text-muted-foreground">Records</p>
                  <p class="font-semibold">{{ detailRes.recordCount }}</p>
                </div>
                <div>
                  <p class="text-muted-foreground">Update Frequency</p>
                  <p class="font-semibold">{{ detailRes.updateFrequency }}</p>
                </div>
                <div>
                  <p class="text-muted-foreground">License</p>
                  <p class="font-semibold">{{ detailRes.license }}</p>
                </div> -->
              </div>
            </div>

            <!-- Contact -->
            <!-- <div class="bg-card border-border rounded-lg border p-6">
              <h3 class="mb-4 text-lg font-bold">Contact</h3>
              <p class="text-muted-foreground mb-4 text-sm">
                For questions or support:
              </p>
              <p class="text-primary font-mono text-sm">
                {{ detailRes.contact }}
              </p>
            </div> -->

            <!-- Actions -->
            <div class="space-y-3">
              <button
                class="bg-primary text-primary-foreground flex w-full items-center justify-center gap-2 rounded-lg px-4 py-3 font-semibold text-white transition-opacity hover:opacity-90"
                @click="onDownload"
                :disabled="isDownloading"
              >
                <Icon name="lucide:download" class="h-5 w-5" />
                {{ isDownloading ? 'Đang tải...' : 'Tải dữ liệu' }}
              </button>
              <!-- <button
                class="border-border hover:bg-muted flex w-full items-center justify-center gap-2 rounded-lg border px-4 py-3 font-semibold transition-colors"
              >
                <Icon name="lucide:share-2" class="h-5 w-5" />
                Share
              </button> -->
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
