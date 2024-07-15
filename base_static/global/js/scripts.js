(() => {
    const menuContainer = document.querySelector('.menu-container');
    const showMenu = document.querySelector('.button-show-menu');
    const closeButton = document.querySelector('.button-menu-close');

    showMenu.addEventListener('click', () => {
        showMenu.classList.toggle('show-menu-button-visible');
        menuContainer.classList.toggle('menu-container-hidden');
    })

    closeButton.addEventListener('click', () => {
        showMenu.classList.toggle('show-menu-button-visible');
        menuContainer.classList.toggle('menu-container-hidden');
    })

})();

(() => {
    const logoutForm = document.querySelector('.logout-form');
    const logoutButton = document.querySelectorAll('.loggout-button')[0];

    logoutButton.addEventListener('click', e => {
        e.preventDefault();

        logoutForm.submit()
    })
})()

function deleteConfirm(element) {
    const body = document.body
    const mainList = document.querySelector('.main-content-list')
    const form = element.parentNode
    const confirmBox = document.querySelector('.message-box')
    
    body.classList.add('overflow-hidden')
    mainList.classList.add('message-focus-event')
    confirmBox.classList.add('message-focus')
    
    confirmBox.addEventListener('click', e => {
        if (e.target.id === 'confirm-button-yes') {
            form.submit()
        } else if (e.target.id === 'confirm-button-no') {
            body.classList.remove('overflow-hidden')
            mainList.classList.remove('message-focus-event')
            confirmBox.classList.remove('message-focus')
        }
    })

}

function back(url) {
    window.location.replace(url)
}

function charCount(element) {
    const bioArea = element
    const charCount = document.querySelector("#current-char")

    const maxLength = bioArea.getAttribute("max-length")
    const remainingChars = maxLength - bioArea.value.length

    if (remainingChars <= 0) {
        bioArea.value = bioArea.value.substr(0, maxLength)
    }
    charCount.textContent = `${remainingChars}/${maxLength}`
}

function functinText(element) {
    const form = element.parentElement
    const bioText = document.querySelector("#text-bio")
    const button = document.querySelector(".profile-button")
    const remainingChars = document.querySelector('#current-char')

    form.addEventListener("submit", e => {
        e.preventDefault()

        if (!bioText.classList.contains('show-bio')) {
            form.submit()
            return
        }

        bioText.classList.remove("show-bio")
        bioText.removeAttribute("readonly")
        bioText.focus()
        bioText.setSelectionRange(bioText.value.length, bioText.value.length)

        remainingChars.classList.remove("hidden")
        charCount(bioText)
        button.innerHTML = '<i class="fa-solid fa-pencil"></i>  Send'
    })
}

function isCurrentType(fileInput, acceptTypes=['image/png', 'image/jpeg']) {
    const currentFile = fileInput.files
    if (currentFile.length === 0) {
        return false
    }

    if (acceptTypes.includes(currentFile[0].type)) {
        return true
    }
}

function chooseFile() {
    // This function requires an element with id fileInput to act

    const fileInput = document.getElementsByName('profile-image-input')[0]
    const imagePortail = document.querySelector('#author-image')
    const saveButton = document.querySelector('.save-image-button')

    let tempURL

    fileInput.click()

    fileInput.addEventListener("change", () => {
       if (!isCurrentType(fileInput)) {
            return
       }

       imagePortail.setAttribute('style', 'border-radius:none;')
       saveButton.classList.remove('hidden')

       tempURL = URL.createObjectURL(fileInput.files[0])
       imagePortail.setAttribute('src', tempURL)
    }, {once: true})
}
