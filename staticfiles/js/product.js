function autoReloadAfterCart(event) {
  setTimeout(() => {
    window.location.reload()
  }, 400)
}

let scale = 1
const img = document.getElementById('productImage')
const MAX_ZOOM = 2.5
const MIN_ZOOM = 1
const STEP = 0.2

function zoomIn() {
  if (scale < MAX_ZOOM) {
    scale += STEP
    img.style.transform = `scale(${scale})`
  }
}

function zoomOut() {
  if (scale > MIN_ZOOM) {
    scale -= STEP
    img.style.transform = `scale(${scale})`
  }
}

function resetZoom() {
  scale = 1
  img.style.transform = 'scale(1)'
}
