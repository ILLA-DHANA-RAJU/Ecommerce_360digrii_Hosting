setInterval(function () {
  const msg = document.getElementById('id1')
  if (msg) {
    msg.style.display = 'none'
  }
}, 10000)

function acc() {
  const vis = document.getElementById('id2')
  if (vis) {
    vis.style.display = 'block'
  }
}

function autoReloadAfterCart(event) {
  setTimeout(() => {
    window.location.reload()
  }, 100)
}
