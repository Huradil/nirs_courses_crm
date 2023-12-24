/**
 * Get a element.
 * @param {string} mark1
 * @param {Object} options
 * @param {string} mark2
 * @returns
 */
function getElement(mark, options = {}) {
  const { many = false } = options
  if (many) {
    return document.querySelectorAll(mark)
  }
  return document.querySelector(mark)
}


/**
 * Create a plus component.
 * @param {string} name
 * @param {string} dataTarget
 * @returns {HTMLDivElement}
 */
function createPlus(name, dataTarget) {
  const html = `<div class="input-group-prepend" data-toggle="modal" data-target="#${dataTarget}">
    <span class="input-group-text" id="basic-addon1"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-square" viewBox="0 0 16 16">
    <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
  </svg></span>
  </div>`
  const div = document.createElement('div')
  div.classList.add('input-group', 'mb-3', 'input-group-row')
  div.id = `form-group__${name}`
  div.innerHTML = html

  return div
}

/**
 * Add a plus to froms.
 * @param {HTMLDivElement} formGroup
 * @param {string} dataTarget
 */
function addPlusToForm(formGroup, dataTarget) {
  const labelFor = formGroup.querySelector('label').getAttribute('for')
  const createBtn = createPlus(labelFor.split('_')[1], dataTarget)
  const input = getElement(`#${labelFor}`)
  formGroup.insertAdjacentElement('beforeend', createBtn)
  createBtn.insertAdjacentElement('afterbegin', input)
}