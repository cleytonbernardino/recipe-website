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

function back(url){
    window.location.replace(url)
}
