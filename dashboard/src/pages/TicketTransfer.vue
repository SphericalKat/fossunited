<template>
  <Header />
  <div class="w-full flex items-center justify-center">
    <TransferSuccess v-if="inSuccess" />
    <div v-else class="max-w-screen-xl w-full p-5">
      <img v-if="transfer_settings.doc?.banner_image" :src="transfer_settings.doc.banner_image" alt="" class="object-cover hidden md:block w-full border rounded-lg aspect-[4.96/1]">
      <div class="mt-8">
        <div class="prose min-w-full">
          <div class="text-base uppercase font-medium text-gray-600 mb-2">
            Portal
          </div>
          <h1 class="m-0">Ticket Transfers</h1>
          <div
            v-if="transfer_settings.doc"
            v-html="transfer_settings.doc.web_page_description"
          ></div>
        </div>
      </div>
      <div class="bg-white p-6 rounded border w-full">
        <div class="flex flex-col md:grid md:grid-cols-2 gap-4">
          <div class="col-span-2 flex flex-col gap-2">
            <div class="prose">
              <h4>Ticket Details</h4>
            </div>
            <div class="w-full flex flex-col md:grid md:grid-cols-2 gap-4">
              <FormControl
                size="sm"
                label="Ticket ID  &ast;"
                v-model="ticketId"
                type="text"
                @focusout="
                  () => {
                    isTicketValid()
                  }
                "
              />
              <div class="hidden md:block"></div>
              <div
                v-if="ticket.data && event.data"
                class="col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                <FormControl
                  label="Event"
                  v-model="event.data.event_name"
                  type="text"
                  :disabled="true"
                />
                <FormControl
                  label="Ticket Tier"
                  v-model="ticket.data.tier"
                  type="text"
                  :disabled="true"
                />
              </div>
            </div>
            <ErrorMessage :message="ticketValidateError" />
          </div>
          <div class="col-span-2">
            <hr />
          </div>
          <div class="col-span-2 prose">
            <h4>Receiver Details</h4>
          </div>
          <FormControl
            v-model="receiver.receiver_email"
            label="Receiver Email &ast;"
            type="email"
            size="sm"
            placeholder="john@fossunited.org"
          />
          <FormControl
            v-model="receiver.receiver_name"
            label="Receiver Name &ast;"
            type="text"
            size="sm"
            placeholder="John Doe"
          />
          <FormControl
            v-model="receiver.designation"
            label="Designation"
            type="text"
            size="sm"
            placeholder="SDE"
          />
          <FormControl
            v-model="receiver.organization"
            label="Organization"
            type="text"
            size="sm"
            placeholder="FOSS United"
          />
          <FormControl
            v-if="receiver.wants_tshirt"
            v-model="receiver.tshirt_size"
            label="T-Shirt Size"
            type="select"
            size="sm"
            :options="['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL']"
          />
          <div class="col-span-2">
            <ErrorMessage :message="ticketErrors" />
          </div>
          <div></div>
          <div class="flex items-end justify-end">
            <Button
              class="w-full md:w-2/3 font-medium"
              label="Initiate Transfer"
              variant="solid"
              theme="green"
              size="md"
              @click="initiateTranfer"
              :disabled="ticketValidateError != ''"
              :loading="createTransferDoc.loading"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import Header from '@/components/Header.vue'
import TransferSuccess from '@/components/TransferSuccess.vue'
import {
  createDocumentResource,
  FormControl,
  ErrorMessage,
  createResource,
  usePageMeta,
} from 'frappe-ui'
import { reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

usePageMeta(() => {
  return {
    title: 'Ticket Transfers',
  }
})

const inSuccess = ref(false)

const transfer_settings = createDocumentResource({
  doctype: 'Ticket Transfer Settings',
  name: 'ticket_transfer_settings',
  auto: true,
})

const ticketValidateError = ref('')
const ticketErrors = ref('')

const ticketId = ref('')
const receiver = reactive({
  receiver_email: '',
  receiver_name: '',
  designation: '',
  organization: '',
  wants_tshirt: false,
  tshirt_size: '',
})

const ticket = createResource({
  url: 'fossunited.api.tickets.get_ticket_details',
  makeParams() {
    return {
      ticket_id: ticketId.value,
    }
  },
  onSuccess(data) {
    event.fetch()
    receiver.wants_tshirt = data.wants_tshirt
    if (data.tshirt_size){
      receiver.tshirt_size = data.tshirt_size
    }
  },
})

const event = createResource({
  url: 'frappe.client.get',
  makeParams() {
    return {
      doctype: 'FOSS Chapter Event',
      name: ticket.data.event,
    }
  },
})

const isTicketValid = () => {
  if (ticketId.value === '') {
    ticketValidateError.value = 'Ticket ID is required'
    event.data = null
    ticket.data = null
    return false
  }

  createResource({
    url: 'fossunited.api.tickets.check_ticket_validity',
    params: {
      ticket_id: ticketId.value,
    },
    auto: true,
    onSuccess(data) {
      if (!data) {
        ticket.data = null
        ticketValidateError.value = 'Invalid Ticket ID'
        return false
      }
      ticketValidateError.value = ''
      ticket.fetch()
      return true
    },
    onError(err) {
      console.log(err)
    },
  })
}

const transferErrors = () => {
  const errors = []

  if (!ticketId.value) {
    ticketValidateError.value = 'Ticket ID is required'
    errors.push('Ticket ID is required')
  }
  if (!receiver.receiver_email) {
    ticketErrors.value = 'Receiver Email is required'
    errors.push('Receiver Email is required')
  }
  if (!receiver.receiver_name) {
    ticketErrors.value = 'Receiver Name is required'
    errors.push('Receiver Name is required')
  }
  return errors
}

const createTransferDoc = createResource({
  url: 'fossunited.api.tickets.create_transfer_request',
  makeParams() {
    return {
        ticket: ticketId.value,
        receiver_details: {
          receiver_email: receiver.receiver_email,
          receiver_name: receiver.receiver_name,
          designation: receiver.designation,
          organization: receiver.organization,
          wants_tshirt: receiver.wants_tshirt,
          tshirt_size: receiver.tshirt_size,
        }
    }
  },
  onSuccess(data) {
    inSuccess.value = true
  },
  onError(err) {
    toast.error('Failed to initiate transfer. ' + err.message)
  },
})

const initiateTranfer = () => {
  if (transferErrors().length > 0) {
    ticketErrors.value = transferErrors().join(', ')
    return
  }
  createTransferDoc.fetch()
}
</script>
