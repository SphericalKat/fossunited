<template>
  <Dialog
    class="z-50"
    v-model="showDialog"
    :options="{
      title: 'Sold T-shirt Details',
    }"
  >
    <template #body-content>
        <div class="text-sm">
            <p class="mb-2">T-shirts sold for this event.</p>
        </div>
        <table class="w-3/4 table-fixed text-center">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                    <th class="p-2 border">Size</th>
                    <th class="p-2 border">Quantity</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(quantity, size) in insight.tshirt_size_count">
                    <td class="p-2 text-base border">{{ size }}</td>
                    <td class="p-2 text-base border">{{ quantity }}</td>
                </tr>
                <tr>
                    <td class="p-2 text-base font-semibold">Total</td>
                    <td class="p-2 text-base font-semibold">{{ insight.tshirts_sold }}</td>
                </tr>
            </tbody>
        </table>
    </template>
  </Dialog>
  <div class="flex flex-col w-full border rounded-sm p-4">
    <div class="text-sm flex gap-2 items-center uppercase font-semibold">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="currentColor"
        class="icon icon-tabler icons-tabler-filled w-5 h-5 icon-tabler-shirt"
      >
        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
        <path
          d="M14.883 3.007l.095 -.007l.112 .004l.113 .017l.113 .03l6 2a1 1 0 0 1 .677 .833l.007 .116v5a1 1 0 0 1 -.883 .993l-.117 .007h-2v7a2 2 0 0 1 -1.85 1.995l-.15 .005h-10a2 2 0 0 1 -1.995 -1.85l-.005 -.15v-7h-2a1 1 0 0 1 -.993 -.883l-.007 -.117v-5a1 1 0 0 1 .576 -.906l.108 -.043l6 -2a1 1 0 0 1 1.316 .949a2 2 0 0 0 3.995 .15l.009 -.24l.017 -.113l.037 -.134l.044 -.103l.05 -.092l.068 -.093l.069 -.08c.056 -.054 .113 -.1 .175 -.14l.096 -.053l.103 -.044l.108 -.032l.112 -.02z"
        />
      </svg>
      <span> T-shirts Sold </span>
    </div>
    <div class="flex gap-2 items-end justify-between mt-6">
      <div class="prose">
        <h2 class="">{{ insight.tshirts_sold }}</h2>
      </div>
      <Button class="w-fit" label="View Details" @click="showDialog = true" />
    </div>
  </div>
</template>
<script setup>
import { Dialog } from 'frappe-ui'
import { defineProps, ref } from 'vue'

const showDialog = ref(false)

const props = defineProps({
  insight: {
    type: Object,
    required: true,
  },
})
</script>
