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

function deleteConfirmTest() {
    const body = document.querySelector('body')
    const delButtom = document.getElementsByClassName('plaintext-button')[0]
    const form = document.getElementsByClassName('message-box')[0]
 
    body.addEventListener('click', e => {
        e.preventDefault();
        console.log(e.target.classList.contains('yes'))
        form.addEventListener('click', event => {

        if (e.target.classList.contains('yes')) {
            console.log('TRues')
        }
        })
    })
    
}

deleteConfirmTest()