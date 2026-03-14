document.addEventListener('DOMContentLoaded', function () {
  let quty = document.getElementById('qty')
  let totalSpan = document.getElementById('total')

  if (!totalSpan || !quty) return

  const price = Number(totalSpan.dataset.price)

  window.incr = function () {
    if (quty.value >= 4) {
      alert('Your cannot buy more than 4 items.')
      return
    }
    quty.value = parseInt(quty.value) + 1
    updateTotal()
  }

  window.decr = function () {
    if (quty.value > 1) {
      quty.value = parseInt(quty.value) - 1
      updateTotal()
    }
  }

  function updateTotal() {
    totalSpan.innerText = price * quty.value
  }
})

document.addEventListener('DOMContentLoaded', function () {
  let cod = document.getElementById('cod')
  let online = document.getElementById('online')
  let confirmBtn = document.getElementById('confirm-btn')
  let payBtn = document.getElementById('pay-btn')

  function toggleButtons() {
    if (cod.checked) {
      confirmBtn.style.display = 'block'
      payBtn.style.display = 'none'
    } else if (online.checked) {
      confirmBtn.style.display = 'none'
      payBtn.style.display = 'block'
    }
  }

  cod.addEventListener('change', toggleButtons)
  online.addEventListener('change', toggleButtons)
})

// orders handling
const ORDER_STATUS = ['CREATED', 'PENDING', 'PACKED', 'SHIPPING', 'SHIPPED', 'OUT OF DELIVERY', 'DELIVERED', 'EXPIRED']

const PAYMENT_STATUS = ['CASH ON DELIVERY', 'PAID']

function buildSelect(options, selected) {
  let html = `<select class='inline-select'>`
  options.forEach(opts => {
    html += `<option value='${opts}' ${opts === selected ? 'selected' : ''}>${opts}</option>`
  })
  html += `</select>`
  return html
}

$(document).on('click', '.edit-btn', function () {
  let row = $(this).closest('tr')

  let orderStatusTd = row.find('td:eq(4)')
  let paymentTypeTd = row.find('td:eq(5)')
  let paymentStatusTd = row.find('td:eq(6)')

  let orderStatus = orderStatusTd.text().trim()
  let paymentType = paymentTypeTd.text().trim()
  let paymentStatus = paymentStatusTd.text().trim()

  if (orderStatus === 'CANCELLED' && paymentStatus === 'CANCELLED') {
    alert('Cancelled orders cannot be modified')
    return
  }

  orderStatusTd.html(buildSelect(ORDER_STATUS, orderStatus))

  if (paymentType === 'CASH ON DELIVERY') {
    paymentStatusTd.html(buildSelect(PAYMENT_STATUS, paymentStatus))
  } else {
    paymentStatusTd.text(paymentStatus)
  }

  $(this).hide()
  row.find('.save-btn').show()
})

$(document).on('click', '.save-btn', function () {
  let row = $(this).closest('tr')
  let orderId = $(this).data('id')

  let payload = {
    order_id: orderId,
    order_status: row.find('td:eq(4) select').val(),
    payment_status: row.find('td:eq(6) select')?.val() || row.find('td:eq(6)').text().trim(),
    csrfmiddlewaretoken: CSRF_TOKEN
  }

  $.post(UPDATE_ORDER_URL, payload, function () {
    $('#table').DataTable().ajax.reload(null, false)
  })
})
