function deleteConfirm() {
    const forms = document.querySelectorAll('.form-delete');

    for (const form of forms) {
        form.addEventListener('submit', e => {
            e.preventDefault();

            const confirmed = confirm('Are you sure:')

            if (confirmed) {
                form.submit();
            }
        })
    }
  
}

function deleteConfirmTest(element) {
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

function back() {
    window.history.back();
}