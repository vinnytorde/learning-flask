function get(selector) {
  return document.querySelector(selector)
}

function set(){
  console.log('dis',this)
}

function prefill() {
  window.onload = function(){ get('#first_name').set('vinny') }
}

prefill()
