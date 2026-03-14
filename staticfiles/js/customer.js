function activate(el) {
  el.previousElementSibling.removeAttribute('disabled')
  el.previousElementSibling.focus()
}

function allactivate() {
  const inputs = document.querySelectorAll('.user_details input')
  inputs.forEach(input => {
    input.removeAttribute('disabled')
  })
  if (inputs.length > 0) {
    inputs[0].focus()
  }
}

function allupdate() {
  const fields = document.querySelectorAll('.input-box input, .input-box select, .input-box textarea')

  fields.forEach(field => {
    field.removeAttribute('disabled')
  })

  if (fields.length > 0) {
    fields[0].focus()
  }
}
