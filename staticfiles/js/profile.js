function del() {
  return confirm('Are you want to delete Your Profile?')
}

function pdel() {
  return confirm('Do you want to delete the product?')
}

setTimeout(function () {
  const update = document.getElementById('id1')
  if (update) {
    update.style.display = 'none'
  }
}, 2000)
